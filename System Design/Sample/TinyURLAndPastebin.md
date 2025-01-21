# Problem requirements

1. Generate a unique short URL per long URL/paste.
   - How can we ensure these are unique?
2. Per generated URL allow the original poster to see the number of clicks.
   - How can we ensure these are accurate?

# Summary

Generating shortlinks.

# Performance considerations

1. Median URL has 10K clicks, most popular URL has millions of clicks.
2. At a time may have to support up to 1 trillion short URLs.
3. For certain pastes, text sizes can be GBs, avg. size is kilobytes.
4. The redirection should occur with minimal delay (< 100ms)
5. The system should be reliable and available 99.99% of the time (availability > consistency)
6. The system should scale to support 100M DAU

Back of the envelope math:
1 trillion \* 1 kB = 10^15 => 1 PB

Reads >> Writes - want to optimize these!

![ ](/Resources/images/tinyurl.png)

# Defining the Core Entities

In a URL shortener, the core entities are very straightforward:

1. Original URL: The original long URL that the user wants to shorten.
2. Short URL: The shortened URL that the user receives and can share.
3. User: Represents the user who created the shortened URL.

# API

REST API:

- POST: Create a new resource
- GET: Read an existing resource
- PUT: Update an existing resource
- DELETE: Delete an existing resource

To shorten a URL, we’ll need a POST endpoint that takes in the long URL and optionally a custom alias and expiration date, and returns the shortened URL. We use post here because we are creating a new entry in our database mapping the long url to the newly created short url.

```markdown
// Shorten a URL
POST /urls
{
"long_url": "https://www.example.com/some/very/long/url",
"custom_alias": "optional_custom_alias",
"expiration_date": "optional_expiration_date"
}
->
{
"short_url": "http://short.ly/abc123"
}
```

For redirection, we’ll need a GET endpoint that takes in the short code and redirects the user to the original long URL. GET is the right verb here because we are reading the existing long url from our database based on the short code.

```markdown
// Redirect to Original URL
GET /{short_code}
-> HTTP 302 Redirect to the original long URL
```

# Link generation

Bad idea is to have some number and monotonically increasing sequence number for all of the shortlinks
but then you need to lock on that number each time for every single request that everyone is making
so you can actually generate that shortnumber.

Idea: We want to generate those links equally across our system, a way to do this is using a hashing function.
In order to achieve very evenly distributed links we can pass long url, user id, create timestamp.

Hash functions also provide a high degree of entropy, meaning that the output is random and unique for each input and unlikely to collide.

> h(long url, user id, create timestamp) = tinyurl.com/31jkj5gjk

How many characters do we actually need? Assuming we are using 0-9 (10 chars) and a-z (26 chars) => 36.
So possibilities are 36^n if we use above chars.
If n = 8 we have arount 2 trillion combinations 36*36*36\*...

Hashing is a process of converting data of any size into a fixed size. It is a crucial technique in cryptography and data security. Hashing algorithms like SHA-256 produce a fixed-size output, which can be converted into Base 36 to make it more human-readable.

Hash collisions? In a database we can't really use a linked list. That is why we can handle collisions with probing.

# Assigning URLs

Writing those URLS - assigining them. What type of replication do we need to use within our databases?
We want to maximize our write throughput whenever possible.

## Replication

Can we do so with replication? Can we use multi-leader or leaderless replication? No!
Why? Imagine having two URL being submitted for generation to the database at the same time.
At the same time we have the same short link. As a result we have a conflict.
It's arbitrary how you end up resolving which write is going to win.
Imagine using LWW (last write wins) - and the second URL has a greater timestamp (you can't trust timestamps),
then it will be stored.
We can inform the other client that it's no longer valid. But for most user experiences this won't work here.

This exclides all databases that use leaderless replication - Cassandra, Riak, etc.

We want to be using single-leader replication.

## Caching

Sometimes we can speed up our writes using a write back cache.
The jist is we can first write to them and eventually at some point in time we can flush those out.
But what we enconter here is basically the same problem we encountered above with multi-leader/leaderless replication.
No one really knows the second they make the write whether their link is valid or not.

With this type of approach we run into the same issue as before!

## Partitioning

Not only is partitioning very important if we have a lot of data, it can help us speed up our reads and writes by reducing load on every node.

Can partition by range of short URL, they're already hashed so should be relatively even.

- Allows probing to another hash to stay local to one DB. This means you don't have to go to another partition randomly to make that right and
  it should in theory increase latency.
- Keep track of consistent hashing on coordination service, minimizes reshuffling on cluster size change. Whenever the cluster size changes, fewer keys are
  going to have to be redistributed.

## Single node

| tiny URL  | actual URL   | user ID | create time | expire time | clicks |
| --------- | ------------ | ------- | ----------- | ----------- | ------ |
| 345gne3de | facebook.com | 22      | 11/11/2011  | 12/12/2022  | 500    |
| 567gne3dv | google.com   | ------- | ----------- | ------      |        |
| 987gne3dv | siteA.com    | ------- | ----------- | ------      |        |
| 987gne3dv | siteB.com    | ------- | ----------- | ------      |        |

Ideally, tiny URL needs to be unique. Imagine we have two users, in theory they can be adding the same row with the same URL
for the short URL at the same time and our database woudn't be able to do anything about it. Why? Normally, you would want to be
locking on this key but in our case this row didn't actually exist yet before they added them and so we don't have anything to lock on.

So how can a database internally actually do something like that? There are two possible solutions.

### Predicate locks

Locks on rows that don't exist yet.

Predicate Query: Select \* from URLs where TinyURL = "987gne3dv"

- Predicate queries can be expensive. Because they have to go through the whole database and actually find all of the rows that
  potentially apply. Something that can make this a little bit faster is using an index on the short URL field. Why?
  Because an index basically means that tinyURL will be sorted internally, now all of our queries will be O(lon (N) vs O(n))
- Using a stored procedure can reduce network calls in event of hash collision! We have two network calls by the client who lost
  the race conditioning and now has to try to get link X + 1. Stored procedure is an advanced database function that where if X is taken, grab X + 1.
  That way we can do all of that writing with just one network call, perhaps it would speed things up.

### Materializing conflicts

As opposed to locking on rows that don't exist yet, what if we actually just grab the lock on rows that do exist. How can they exist? We basically write every single possible key to the database. So now keys exist to lock on!

> 2 trillion _ 1 byte/char _ 8 chars = 16 TB

not very much.

## Engine implementation

We don't need range queries, so a hash index would be super fast, but we're storing 1 PB of data so probably too expensive for in-memory DB.

So if we are limited with on-disk we are limited with two choices:

1. **LSM Tree + SSTable**. The LSM Tree is going to be worse for reads because when you read you typically have to read from multiple SSTables and possibly
   the LSM tree as well. And when you write, you are writing basically to your LSM tree which is in memory.
2. **B-tree**. You are writing straight to disk which is a little bit less efficient but when you are reading you only have to traverse the tree one time. There is no concept of having to check multiple different files and so a B tree is literally going write-through. Finding the piece of data - it's all
   sorted and then you are good to go.

In our case we are prioritizing reads over rides, so we can opt for the B tree.

## Database choice

So far we have:

1. Single-leader replication.
2. Partitioned.
3. B-tree based index.

Seems easy to just use a relational DB, we're not making any distributed joins anyway. MySQL.

# Maximizing Read speed

## Adding an Index

To avoid a full table scan, we can use a technique called indexing. Think of an index like a book's table of contents or a library's card catalog. It provides a quick way to find what we're looking for without having to flip through every page or check every shelf. In database terms, an index creates a separate, sorted list of our short URLs, each with a pointer to where the full information is stored in the main table. This allows the database to use efficient search methods, dramatically reducing the time it takes to find a matching URL.

1. B-tree Indexing: Most relational databases use B-tree indexes by default. For our URL shortener, we'd create a B-tree index on the short code column. This provides O(log n) lookup time, which is very efficient for large datasets.
2. Primary Key: We should designate the short code as the primary key of our table. This automatically creates an index and ensures uniqueness. By making the short code the primary key, we get the benefits of both indexing and data integrity, as the database will enforce uniqueness and optimize queries on this field.
3. Hash Indexing: For databases that support it (like PostgreSQL), we can use hash indexing on the short code column. This provides O(1) average case lookup time, which is faster than B-tree for exact match queries (as is our use case)

With these optimizations in place, our system can now find the matching original URL in a fraction of the time it would take without them. Instead of potentially searching through millions of rows, the database can find the exact match almost instantly, greatly improving the performance of our URL shortener service.

### Challenges

Relying solely on a disk-based database for redirects presents some challenges, although modern SSDs have significantly reduced the performance gap. While disk I/O is slower than memory access, it's not prohibitively slow. **A typical SSD can handle around 100,000 IOPS** (Input/Output Operations Per Second), which is quite fast for many applications.

However, the main challenge lies in the sheer volume of read operations required. With 100M DAU (Daily Active Users), assuming each user performs an average of 5 redirects per day, we're looking at:

100,000,000 users \* 5 redirects = 500,000,000 redirects per day
500,000,000 / 86,400 seconds ≈ 5,787 redirects per second

This assumes redirects are evenly distributed throughout the day, which is unlikely. Most redirects will occur during peak hours, which means we need to design for high-traffic spikes. **Multiplying by 100x to handle the spikes means we need to handle ~600k read operations per second**.

Even with optimized queries and indexing, a single database instance may struggle to keep up with this volume of traffic. This high read load could lead to increased response times, potential timeouts, and might affect other database operations like URL shortening.

## Replication and Partitioning

Replicas + multiple partitions to ensure adequate ability to handle load. Not only for fault tolerance but to speed up reads as well.
Replications will allow us to read from our follower replicas as well as our leader. Also for every partition we will have less load
as a result of the fact there are now more places to actually read from.

Worth noting that in this case of single leader replication because we are going to use asynchronous consistency or eventual consistency
it is possible that a client could lead by a follower, get some stale data, where maybe there is no actual URL to redirect you to. Where in reality there has been, but just not replicated yet.

We need to be careful with this. Not to add logic in the application to check the leader replica. Could accidently spam leader.

## Hot Links

Some links are "hot", they get much more traffic than other.

A caching layer can help mitigate some of the load!

- Caching layer can be scaled independenly of DB.
- Partitioning the cache by short URL should lead to fewer cache misses.

## Populating the cache

When talking about caching, CDNs, there are two concepts we have to consider. We can either push the data in advance when it's created. Or we can pull it in there. We can't push links to the cache in advance, we don't know what will be popular. So how should we populate it?

- Write back - can have write conflicts. It can lead to data inconsistencies.
- Write through - in addition to writing to the database, you also write in your cache. If you need to, you can use 2PC to make sure that they always stay in line. But anyway, it will slow the write speed and the vast majority of those links we don't even want in our cache.
- Write around - write to DB as usual and when people read from the cache the DB will send its results first to the cache and then to the user.

LRU eviction policy can be used - least recently used.

To improve redirect speed, we can introduce an in-memory cache like Redis or Memcached between the application server and the database. This cache stores the frequently accessed mappings of short codes to long URLs. When a redirect request comes in, the server first checks the cache. If the short code is found in the cache (a cache hit), the server retrieves the long URL from the cache, significantly reducing latency. If not found (a cache miss), the server queries the database, retrieves the long URL, and then stores it in the cache for future requests.

The key here is that instead of going to disk we access the mapping directly from memory. This difference in access speed is significant:

- Memory access time: ~100 nanoseconds (0.0001 ms)
- SSD access time: ~0.1 milliseconds
- HDD access time: ~10 milliseconds

This means memory access is about 1,000 times faster than SSD and 100,000 times faster than HDD. In terms of operations per second:

- Memory: Can support millions of reads per second
- SSD: ~100,000 IOPS (Input/Output Operations Per Second)
- HDD: ~100-200 IOPS

### Challenges

While implementing an in-memory cache offers significant performance improvements, it does come with its own set of challenges. Cache invalidation can be complex, especially when updates or deletions occur, though this issue is minimized since URLs are mostly read-heavy and rarely change. The cache needs time to "warm up," meaning initial requests may still hit the database until the cache is populated. Memory limitations require careful decisions about cache size, eviction policies (e.g., LRU - Least Recently Used), and which entries to store. Introducing a cache adds complexity to the system architecture, and you'll want to be sure you discuss the tradeoffs and invalidation strategies with your interviewer.

## CDNs

Another thing we can do to reduce latency is to utilize Content Delivery Networks (CDNs) and edge computing. In this approach, the short URL domain is served through a CDN with Points of Presence (PoPs) geographically distributed around the world. The CDN nodes cache the mappings of short codes to long URLs, allowing redirect requests to be handled close to the user's location. Furthermore, by deploying the redirect logic to the edge using platforms like Cloudflare Workers or AWS Lambda@Edge, the redirection can happen directly at the CDN level without reaching the origin server.

# Analytics

We keep a clicks counter per row, could we just implement it? Without any sort of locking there is going to be a race condition. Why? Each participant
might see an old value (i.e. 100), and say - increment to 101. For very popular links this is a real possibility. When you are implementing locking or
atomic operations for something that is popular enough the database might not be able to handle that. This is too slow for popular links.

## Stream processing

Idea: we can place individual data somewhere that doesn't require grabbing locks, and then aggregate them later.

Options:

- Database -> Relatively slow
- In memory message broker -> super fast, not durable
- Log based message broker -> Basically writing to write ahead log, durable.

We can use kafka.

## Click consumer

The consumer of these events - how is it that once we have the events placed in some sort of queue that we can go ahead and process them. What technology
do we want to use to do so?

Options:

- HDFS + Spark - dump to HDFS or S3 and do a batch job on it. Batch jobs to aggregate clicks, may be too infrequent.
- Flink - More of a real-time solution. Processes each event individually, may send many writes to the database depending on the implementation.
- Spark streaming - natively supports mini-batching which is configurable. We can just say "give me mini batch of 100 clicks". As a result every single 100 clicks will go and write to the sink in that type of intervals.

Stream consumer frameworks enable us to ensure exactly once processing of events via checkpoint/queue offsets! Between every event that gets to kafka and our actual eventual stream consumer, all of those events are only going to be processed once.
However, that is going to break down whenever you have some external system like a DB.

## Exactly once

Do things actually get run exactly once and is it possible to have a certain race conditions that can cause us to have an incorrect click count?

Events are only processed exactly once internally.

Options:

1. Two-phase commit - super slow.
2. Idempotency key - scales poorly if many publishers for the same row. For example if we have 10 spark steaming consumers. And they are all publishing
   to the DB. Now we need to store idempotency key for each publisher.

## One publisher per row

By partitioning our Kafka queues and Spark streaming consumers by short URL we can ensure that only one consumer is publishing clicks for a short ID at
a time. Benefits:

- Fewer idempotency keys to store
- No need to grab locks on publish step.

# Deleting expired links

Can run a relatively inexpensive batch job every X hours to check for expired links.
This only has to grab a lock on row currently being read.

The most expensive batch jobs are the ones that have to grab locks on everything (i.e. aggregation). So a simple cron-job can do the above work.

```python
if (currentTime > row.expiredTime):
    row.delete() / row.clear()
```

# Pastebin - Huge pastes

For pastes that are multiple GB, we cannot store them in our DB.

- Could store them in HDFS (expensive and we don't need the data locality to run batch jobs where our pastes are stored because there are no
  batch jobs to actually run on them)
- Object store likely preferable, cheaper
- CDNs will greatly improve latency, if these massive files are infrequently enough a write through model could make sense.

Writing in series allows us to avoid 2PC.
From the client, first write to CDN, then if that succeeds, write to S3, and if that succeed write to DB. The reason to not write to the database
first and then S3 and CDN is that if the database write goes through, and then the write to S3 fails, it's going to seem that a paste exists when the
data for it actually doesn't. So it's more important to get the data uploaded to our Object store and our CDN first and then after that we can go and
talk about putting things in the database.

You may note that I am actually writing CDN before pulling things - because write through actually makes a lot of sense. At the end of the day, if we
use write around, we're going to have a cache miss which is going to be gigantically expensive for a 10 GB file. So it would be greatly beneficial for us if that was already in the CDN considering how few writes there are relative to reads.

# References

- Jordan has no life youtube
- hellointerview youtube

# Curiousities

How to create the mapping /urls
Validator to check is URL is valid
How do SE works? (i.e. redirects)

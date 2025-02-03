# Load Balancing

## What is a load balancer?

As systems scale, there reaches a point where we can't use more powerful hardware (vertical scaling), so our option is to provide more nodes (horizontal scaling). Application servers can be horizontally scaled. Any time there are a variety of nodes in a cluster that can serve the same request, using a load balancer we can ensure that none of those independent nodes becomes overwhelmed.

Load balancing is the process of distributing incoming traffic across a pool of resources to ensure efficient handling of requests. In the modern world, applications are often composed of multiple resources. With high volumes of data and users, it is essential to handle requests efficiently. To achieve this, server data is often replicated to improve accessibility and ensure availability.

A load balancer is a public-facing component that accepts incoming requests and distributes them across application servers. It acts as an invisible facilitator, ensuring that application servers are utilized effectively and evenly, which helps maintain performance and prevent overloading any single server.

## Why do we load balance? What are the benefits of load balancing?

Load balancers are reverse proxies who direct user traffic to application server traffic.
Advantages include scalability, performance, security, availability.

- _Scalability_: The application can handle thousands of requests with the help of load balancers. The load balancer can route requests to many servers so that no server becomes a bottleneck. It can predict application traffic so we can add or remove service instances and utilize resources.
- _Performance_: The load balancers can distribute the traffic evenly between servers and they can also redirct traffic to servers which are geographically closer to reduce latency.
- _Security_: Load balancers also include security features - they can detect denial of service attacks where maliscios actors flood the system with many concurrent incoming requests which aim to put the system down. They can monitor traffic and block maliscious content. They can also route the traffic to firewalls for additional security.
- _Availability_: Load balancers can detect if a specific server is down and direct traffic to an available service to reduce downtime which increases the fault tolerance of the system.

## What about disadvantages of load balancing?

Load balancers add complexity to our system as they are a new component which has been introduced. Additionally, they are a single point of failure for our system - if the load balancer is down, the trafiic won't be served to the application servers.

## What are the algorithms that they use to decide where traffic goes?

Load balancers direct traffic based or policies or rules to determine which server should handle the current incoming requests. There are two types of algorithms that can help achieve these:

### Static policies

Static load balancing algorithms follow concrete rules to decide a server. They are not based on metrics of the servers and its state. Their main advantage is simplicity. But their cons are less adaptability and precision.

- Round robin: rotate requests evenly accross the server.
- Sticky round robin: same as round robin but with the addition that for some user's requests, all of his/hers requests go to the same server. This can improve performance by having related data to be on the same server. But newly arrived users are assigned randomly to a server, so uneven load can occur.
- Weighted round robin: some servers can have more priority than another. So those with higher priority can receive more traffic compared to the others. The downside is that those weights are manually configured which is less adaptive to changes.
- IP hash: Hash function accepting client IP or request url and routing evenly to servers (uniformly distributed based on the hash function properties).

### Dynamic policies

Those types of algorithms are more adaptive, because they take server conditions into account when distributing requests.

- Least connections: send requests to the server with the least amount of active connections or open requests. However, those require tracking metrics of the servers, which can be delayed if one server becomes overwhelmed or a specific request takes a lot of processing time.
- Least response time: Route requests to servers with lowest current latency or fastest response time. Latency is continuously measured to decide where to route requests. This constant monitoring, however, introduces complexity.

## What are the types of load balancing?

We can classify the load balancers based on what they check from the incoming requests.

### Application load balancing

The application load balancers check data from the request i.e. the header or session ID to redirect traffic.

#### HAProxy

HAProxy is a free, very fast and reliable reverse-proxy offering high availability, load balancing, and proxying for TCP and HTTP-based applications.

#### NGINX

It is a web server that can also be used as a reverse proxy, load balancer and HTTP cache.

#### Traefik

HTTP reverse proxy and load balancer that makes deploying microservices easy. Cloud-native.

### Network load balancers

Network load balancers check network data like the source IP address

### Global server load balancing

Global server load balancing occurs when we have geographically distributed servers.

- Akamai Global Traffic Manager - routes traffic based on geographic location and server health

### DNS load balancers

You configure your domain to route network requests accross a pool of resources on your domain.

- Cloudflare load balancing, offers DNS-based and anycast based load balancing

## Application Gateway

### Security

Input Validation
Rate Limiting / Throttling
Authorization / Authentication
Whitelist / Blacklisting
Flow Control
Authentication (OAuth 2.0)
Request Header Validations
TLS Termination
Request Deduplication
Metering / Usage data collection
Request Dispatching

## Frontend Servers

## CDN / Edge Servers

# Databases

# Indexes

Reads are faster, writes are slower.

## Hash indexes

- They are basic hashmaps in memory. (NOT disk - as we need random hashmap access instantly and not seek it)
- Thus limited by memory space, expensive
- To add durability, we add WAL - write to disk as log (easy as pointer is always at the end) and then write to the hashmap

Pros:

- Fast reads and writes
- reads/writes are constant (write ahead log)

Cons:

- Bad for range queries - range queries take O(n) time
- keys must fit in memory

## B tree indexes

Self-balancing tree on disk.
Hence NO limit on size
Durability can be ensured by NOT updating tree in place, rather updating the pages/block separately file and then updating the reference later on.

Pros:

- No limit to database size
- Good for range queries (as stored in tree structure)
- Reads are fast - O(LogN) to retrieve, but slow writes

Cons:

- writes are slower
- Writes are not that fast - may cause a write to the bottom of the tree, which needs to traverse all the way back up the tree to switch references on disk
- Slower reads than “Hash index” technique as - disk vs memory speed.

## LSM tree indexes

LSM tree: log structure merge tree.
Optimized for fast writes.
Writes are batched in memory as they arrive in a structure (Memtable).
A Memtable is ordered by object key and is implemented as: In-memory tree table (AVL, red-black), self balanced
When reaches a sertain size it is flushed to disk as an immutable Sorted Search Table (SSTable).

- Stores the key-value pairs in a sorted sequence.
- These writes are sequential I/O -> fast.
- The new SSTable becomes the most recent segment of the LSM tree.

- Little faster writes compared to B-Trees, but slower than hash index
- Slower reads speeds than B-Trees, as it has to check all SStables (Also slower range queries)
- Durability handled by WAL - which can be replayed later
- Space concern of LSM trees as in-memory, However we have SStables which are outputted to disk
- Hence No of keys limit not a concern (to store by space)
- SSTable - sorted, immutable
- Finding key - can go on taking time - it is first checked in tree (memtable) and only then across SSTable backwards from creation time
- To delete, its implemented by _tombstone_ value - indicating deleted. It is added to the latest SSTable entry

LSM Optimizations - Merging and compaction:

- Compaction - Merges SSTables in background - O(N) operation - Cons is extra CPU processing in background could be bad
- Similar to merge sort's merge - O(N)
- When merged organized into levels
- Strategies:
  - Size tiered compaction (Cassandra) - write throughout
  - Leveled compaction (RocksDB) - read Optimized

Other:

- Use Sparse index - Also known as index for SSTable
  Take “certain” keys of SSTable and create a sparse index with corresponding stored memory location. - Can use binary search to find in-between keys
- Bloom Filters - Can vaguely tell, if certain “key” present in the SSTable
- Summary table - min/max range of each disk block of every level

# ACID

When writing to certain DBs the DBs provide abstractions that guarantee that properties will hold.
Those properties are called ACID where A is atomicity, C is consistency, I is isolation, D is durability.

- Atomicity means that in a transaction either all writes succeed or none of them do.
- Consistency means that if the transaction fails, data won't be left in an invalid state.
- Isolation is related to race conditioning - if multiple writes appear in the DBs they will be run
  in a way as if they independent from one another. Databases are multithreaded.
- Durability means that when a transaction is commited it will be saved on the disk. The data won't get lost.

This can be achieved using WAL.

Different isolation levels in DBs. Isolation levels determine how much of your transaction is
affected by other concurrent transactions. The higher the isolation level, the less affected
it is. But there is a tradeoff between data accuracy and performance: higher levels of
isolation give higher accuracy, but possibly at a slower speed.

There are four possible isolation levels defined in the ANSI SQL standard. These levels
are designed to balance the need for concurrency and performance with the need for
consistency and accuracy.

## Isolation: Read commited

When a transaction commits, it means the transaction has successfully completed all its
operations and its changes to the database are permanently saved. This marks the end of the
transaction, ensuring that its effects are visible to other transactions and will persist
even in the event of a system crash.

When a DB implements read commited isolation it guarantees that it won't read from a state of dirty read
or dirty write, forms of race conditions. (protected from them)

### Dirty write

This race condition occurs when one process wants to wirte to a row and starts, another one wants to
write as well and overwrites parts of the data and when both commit the state becomes inconsistent.
This can be avoided using row-level locks.
Now when the first process writes to the row it obtains the key and the other process needs to wait for
the first one to commit before obtaining the lock.

### Dirty reads

This race condition occurs when one process starts a transaction and updates a value, then another transaction
starts and reads this updated value, but the first transaction fails and rollbacks. The second transaction
has read an uncommited state which is invalid.
To avoid this, we can again use locking but locking for reads is causing performance issues because
reads are much faster than writes. So DBs usually create a copy of the old valid data, and return the old data
to other transactions. When the data is commited from the first transaction then the old value is replaced with
the new value.

## Isolation: Snapshot isolation

It protects from repeatable read/read skew.

REPEATABLE READ is the ideal isolation level for read-only transactions.

### Repeatable read

Repeatable read/read skew happens when we read multiple rows. While reading all the rows, the rows we
have read might get outdated because another transaction could have updated them already.
To protect against that, the DB can first - use a WAL and assign a monotonically increasing number
to a transaction - i.e. transaction 1: add this value, t2: another value, etc.
Additionally it keeps a snapshot of all values of a specific row with the transaction number that
updated them, so when we read multiple rows in a given transaction, we take the values only before
that specific transaction and that way new transaction values which commit after the specifc one
won't show their values.

## Isolation: Serializable

Serializable isolation level guarantees that even multiple transactions are executed concurrently,
they will be executed as if they are executed serially by the database.

### Write Skew

Another type of DB race condition. When the database has an invariant we want to be true but this
invariant relies on multiple rows. When we update simoltaneously different rows we break the invariant.
We have row-based locking but it doesn't help us in the context of the whole database table.
So to fix write skew we need to obtain the locks based on the invariant - multiple rows locks.

### Phantom writes

Another type of DB race condition. It occurs when we have some invariant and we need to lock a specific
row to achieve the invariant. But the row doesn't exist so no lock is obtained. When two transactions
write data and commit in the same time, the database becomes in an invalid state.
To fix this we need "Materialized conflicts" - create all the needed rows in advance so now transactions
can obtain locks on them.

### Phantom reads

### Two Phase Locking (pessimistic locking)

### Snapshot serializable (optimistic locking)

SERIALIZABLE is a good choice if:

- Data accuracy is paramount and you don’t want to risk anomalies due to missing FOR UPDATE locks.
- You are able to use abstractions in your application that let you avoid repeating the retry
  loop code throughout the app.
- You have a retry loop at another level that obviates the need for retries in the app server.
  For example, a mobile app will often retry failed API calls to cover for flaky networks,
  and this retry can also cover issues related to serializability.

## Summary

The practical developer understands the tradeoffs for each of the isolation levels.
They choose in part for the anomalies the various levels prevent or allow, but more
importantly for the impact the isolation level will have on their application: Higher
isolation levels ensure data consistency, with a potential performance cost due to
increased conflict and retry rates. Conversely, lower isolation levels like READ UNCOMMITTED
prioritize performance and concurrency at the expense of data accuracy, allowing phenomena
such as dirty reads.

Using lower isolation levels safely requires careful use of explicit locks, while high
isolation levels may require transaction retries to prevent anomalies. This simple
decision framework will help you choose the right isolation level for your application.

# Replication

Replication is the process of adding extra copies of our data i.e. DBs. Helps with:

- redundant data - no data is lost
- increased DB throughput
- increased durability
- placing DBs in regions

Two types of replication:

- synchronous replication (strong consistency)
- asynchronous replication (eventual consistency)

Can be achieved using replication log.
Similar to WAL but contains: id: data, id: data, which can be
replcated. The replicas can be different types of DBs so it makes sense
to use abstractions which all DBs understand like a unique ID.

1. Eventual consistency - weak consistency
   No ordering guarantee

Metrics:

- Data consistency: Lowest
- App availability: High to Highest
- Latency: Low
- Throughput: Highest
- Perspective: Client-centric
- Real Life Examples:

The best and well known example is Internet Domain Name System (DNS) that successfully caters to billions of requests daily. DNS is a hierarchical, highly available system and it takes some time to propagate the update for a given entry across DNS servers and clients.

2. Consistent prefix reads

Dirty Read / Stale Read is possible.
Global ordering guarantee applies for a given piece of data across replicas.

Metrics:

- Data consistency: Low
- App availability: High
- Latency: Low
- Throughput: Moderate
- Perspective: Data-centric

Sports apps which track score of soccer, cricket etc.

3. Session consistency
   Session: It’s an abstract concept to correlate multiple Read and Write operations together as a group. Example: when you login to Amazon for shopping, a session is created internally which keeps track of your activities and browsing history, cart updates for that session. Sessions can be identified with a unique id called session id.

- reading your own write - If a Read R follows a Write W by the same unit of execution, R should see W.
- monotonic read - If we assume, with every write, the version of an object increases, each subsequent Read should see the same or monotonically increasing version of the object.
- write follows read - Consider replying to a tweet. You can only do that when the tweet is already written to the system and is visible to you. Both reading and replying could be done in the same session.
- monotonic writes - Consider editing an Wikipedia article. The system should guarantee that version n + 1 always replaces version n for updates performed by the same client, not the other way around. For other clients, these group of updates could be propagated at a later point in time in order. This can be guaranteed by Monotonic Write within a session.

Session Consistency Metrics:

- Data consistency: Moderate
- App availability: High
- Latency: Moderate
- Throughput: Moderate
- Perspective: Client-centric

Session Consistency Real Life Examples:

- Shopping cart. If you add some item to cart in amazon.in, those items won’t be visible in amazon.co.uk as that’s another session.
- Updating profile picture on social media like Facebook, Twitter. You can see your own updates but there is no guarantee others see it during initial few seconds at least.

4. Causal Consistency

Metrics:

- Data consistency: Moderate
- App availability: High
- Latency: Moderate
- Throughput: Moderate
- Perspective: Data-centric
- Real Life Examples:

You post an important status on Facebook asking for some help. After sometime, you realize there is some mistake in the information provided, you go ahead and update the status. Now your online friends should get the update as soon as possible. They can receive the update at different time depending on how their feeds are formed. If eventual consistency is used, some of your friends may still see the older status with wrong info even after long time. But since the event of updating the status causes feed change of online friends, it can be considered as causal consistency.

5. Bounded Staleness Consistency
   Bounded staleness is very near to strong consistency and an extension to consistent prefix reads guarantee but with the flexibility to configure the staleness threshold of the data. Basically users can define how much stale is stale for their use case.

Metrics:

- Data consistency: High
- App availability: Low
- Latency: High
- Throughput: Low
- Perspective: Data-centric

Real Life Example:

- Stock ticker applications.
- Weather tracking apps.
- Mostly, any status tracking apps should be bounded in staleness.

6. Strong Consistency
   Conceptually, strong consistency is exact opposite to eventual consistency where all the replicas read the same value for a given data item at the same point in time. Certainly, ensuring strong consistency across data center even across multiple nodes in a single data center is expensive.

Strong Consistency Metrics:

- Data consistency: Highest
- App availability: Lowest
- Latency: High / Very High
- Throughput: Lowest
- Perspective: Data-centric
- Strong Consistency

Real Life Examples:

- Financial systems executing order payments flow or billing process.
- E-Commerce Flash sale apps (inventory related apps).
- Ticket booking flow while confirming the ticket.
- Meeting scheduling kind of apps.

https://kousiknath.medium.com/consistency-guarantees-in-distributed-systems-explained-simply-720caa034116

## Single leader replication

leader receives writes - followers have a copy of those writes and serve reads

- many copies of the data - increased durability
- increased read throughput

What problems can occur?

1. If a follower goes down it will catch up using replication log
2. If a leader goes down?
   - Is the leader really down / network issue?
   - Data from leader which was not propagated down to replicas is lost
   - If leader goes back online we now have two leaders - split reign
     ^ can be handled using distributed consensus

## Multi leader replication

In a multi-leader replication we have a few leader nodes (which can have follower nodes). Anyone
can write to any of the leaders.
Writes are propagated asynchronously to the other leaders/followers.
Followers serve read requests.

- More write throughput

Topology: All-to-All

- All leader nodes write to all other leader nodes.
- We want to be sure that all of these writes are not being applied mulitple times on every single database node.
- No guarantee of the ordering

Modify replication log:
ID: Key-Value; Seen by: ...

- Things can get out of order.
- Write conflicts

Conflict avoidance

One easy option is last write wins: use timestamp to decide
But which timestamp?
The client can change its timestamp intentionally - not an option.
The receiver can use its timestamp.

But receiver time is also vulnerable to clock skew. Computers rely on quartz crystal for time.

We can also make network requests to NTP (network time server) - which uses GPS clock for more reliability.
But the latency and response time can alter the received time.

- timestamps aren't very reliable

### Write conflicts

Detecting concurrent writes and how the following approach is better than last write wins.

**Concurrent writes**

- Option 1: last write wins - timestamps aren't very reliable
  What about distributed counter?
- Naive: counter is 1 number. Operations: inc()
- Version vectors. Merging them when some value is greater than the other.
  - Not concurrent: If a version vector, where all of the entries are strictly greater than or equal to
    entries of another vector we have "come after" relationship.
  - Concurrent: When are writes concurrent? When version vectors can't be compared:
    [5, 2, 1] ? [4, 3, 2]
  - Option 2: Store siblings. Have user decide later.
- Option 3: CRDTs - DBs do it automatically. Premise behind conflict-free-replicated-data-types.
  - Operational CRDTs
  - State-based CRDTs

#### **Version Vectors:**

Version vectors are a mechanism used to track the "history" of updates to a distributed system in a way that allows for conflict detection and resolution. Version vectors are not operational CRDTs because their role is limited to tracking causality and detecting conflicts.

How it works: Each replica in a distributed system maintains a version vector, which is essentially a vector (array) of counters. Each counter corresponds to a particular replica and tracks the number of updates made by that replica.
Conflict detection: When replicas synchronize, they compare their version vectors. If a replica's version vector is "out of date" (i.e., there are updates in the other replica's version vector that it hasn't seen yet), this replica needs to merge with the other one.
Use case: Version vectors are useful for tracking causality and detecting concurrent updates. If two replicas update the same piece of data independently, a version vector helps determine whether the updates are causally related or not and helps to identify when a conflict arises.

Advantages:

- Allows precise tracking of causal relationships between updates.
- Can detect conflicts in case of concurrent updates.

Disadvantages:

- Can become large if there are many replicas.
- Does not specify how to resolve conflicts automatically.

### Operational CRDT

- inc O(1) sent over network
  Causally consistent broadcasting systems - no drops, no duplicated messages.

Operational CRDTs (also called operation-based CRDTs) are a type of CRDT where updates (operations) are propagated between replicas, and the system ensures that all replicas apply the same operations in a consistent way, leading to convergence.

Key Characteristics of Operational CRDTs

Operation Propagation:
Instead of propagating the entire state, operations (e.g., increment a counter, add an element to a set) are sent between replicas.
Operations must be commutative, so they can be applied in any order without breaking consistency.

Causal Delivery (Optional):
To preserve causality, operations are often delivered in the same causal order they were generated (using mechanisms like version vectors or vector clocks).

Small Overhead:
Since only operations are sent between replicas (not the full state), operational CRDTs are typically more efficient in terms of network overhead than state-based CRDTs.

Idempotency:
Operations are idempotent, meaning that reapplying the same operation multiple times does not change the result.

Examples of Operational CRDTs

Here are some common operational CRDTs:

**G-Counter (Grow-only Counter):**
A counter that can only be incremented.
Operation: Increment(value) is propagated, and each replica maintains a local counter for its updates.
Use Case: Tracking views, likes, or hits in distributed systems.

PN-Counter (Positive-Negative Counter):
A counter that supports both increments and decrements.
Operation: Increment(value) or Decrement(value) is propagated.
Use Case: Tracking balances in distributed systems (e.g., inventory counts).

G-Set (Grow-only Set):
A set where elements can only be added.
Operation: Add(element) is propagated.
Use Case: Tracking a collection of unique IDs or events.

OR-Set (Observed-Remove Set):
A set that allows elements to be added and removed.
Operations: Add(element) and Remove(element) are propagated.
Internally tracks which elements have been "observed" and "removed" to resolve conflicts.
Use Case: Collaborative tools where items can be added or deleted.

LWW-Register (Last-Writer-Wins Register):
A register that holds a single value, where the latest update "wins."
Operation: Write(value, timestamp) is propagated.
Use Case: Distributed configuration settings.

Advantages of Operational CRDTs
Efficient Network Use: Only the operations are sent, reducing the amount of data exchanged compared to state-based CRDTs.
Low State Overhead: Each replica only stores the result of the operations, not the full history of updates.
Real-Time Collaboration: Enables highly responsive systems with fast updates (e.g., collaborative text editors).

Disadvantages of Operational CRDTs
Reliable Delivery Required:
Operations must be reliably delivered to all replicas, often requiring a causal broadcast mechanism.

No Offline Updates Without State Exchange:
If a replica goes offline, it may miss operations unless another mechanism (e.g., a full state sync) is implemented.

Use Cases
Collaborative Tools:
Real-time collaboration platforms like Google Docs or Figma use operation-based CRDTs to ensure edits by multiple users converge consistently.

Distributed Databases:
Systems like Redis CRDTs use operation-based CRDTs to propagate updates efficiently between replicas in multi-region setups.

IoT Systems:
Distributed IoT systems can use operational CRDTs to track sensor readings or aggregate data across nodes.

### State-Based CRDTs:

- We can have duplicate messages now.
- merge function must be commutative, associative and idempotent
- since order doesn't matter, we can communicate via gossip protocol
  - requires no extra messaging infrastructure
  - no guarantee when messages get to nodes
  - can be big

State-based CRDTs (also known as convergent CRDTs) are a class of CRDTs designed to handle conflict resolution automatically by merging the states of different replicas in a consistent way.

How it works: Each replica maintains a local state that can be updated independently. When replicas synchronize, their states are merged in a way that guarantees convergence (i.e., all replicas eventually reach the same state, assuming no more updates are made).
Conflict resolution: State-based CRDTs employ a merge function that is associative, commutative, and idempotent, which ensures that regardless of the order in which replicas merge, they will eventually converge to the same state.
Use case: State-based CRDTs are useful when you want to ensure that replicas can merge their states in a way that guarantees consistency, without needing to track detailed version information.

Examples: Some common state-based CRDTs include:

- G-Counter (Grow-only counter) – A counter that only allows increments.
- PN-Counter (Positive-Negative counter) – A counter that allows both increments and decrements.
- LWW-Element-Set (Last-Writer-Wins element set) – A set where the last update wins in case of conflict.

Advantages:

- Simpler to implement than version vectors.
- Does not require maintaining and comparing version vectors, reducing complexity.
- Can automatically resolve conflicts through the merge function.

Disadvantages:

- Merge functions must be carefully designed to ensure they meet CRDT properties.
- May not always capture detailed causality as version vectors do.

In summary, version vectors are useful for tracking updates and detecting conflicts in distributed systems, while state-based CRDTs are designed for automatic conflict resolution by merging states in a consistent way. Both approaches are useful in different scenarios depending on whether you prioritize conflict detection or conflict resolution.

| **Feature**              | **Version Vectors**                            | **Operational CRDTs**                              | **State-Based CRDTs**                                    |
| ------------------------ | ---------------------------------------------- | -------------------------------------------------- | -------------------------------------------------------- |
| **Primary Purpose**      | Track causality and detect conflicts.          | Propagate and merge operations automatically.      | Merge states automatically for consistency.              |
| **Conflict Handling**    | Detects conflicts, requires manual resolution. | Resolves conflicts automatically using operations. | Resolves conflicts automatically using state.            |
| **Mechanism**            | Vector of counters, one per replica.           | Applies commutative operations to data.            | Merges entire state using commutative functions.         |
| **Eventual Consistency** | Requires external logic to achieve.            | Built-in through operation propagation.            | Built-in through state merging.                          |
| **Causality Tracking**   | Tracks causality explicitly.                   | Tracks causality implicitly through operations.    | Does not track causality explicitly.                     |
| **Network Overhead**     | Minimal: small vector exchanged.               | Moderate: operations need to be propagated.        | Higher: entire state is exchanged during sync.           |
| **Examples**             | DynamoDB, Git, Cassandra.                      | Counters, collaborative text editing (e.g., OT).   | Redis CRDTs, Riak, collaborative tools like CRDT sets.   |
| **Complexity**           | Simple to implement but lacks resolution.      | Medium: requires well-defined operations.          | Medium to high: requires efficient state representation. |
| **Best Use Case**        | Detecting and diagnosing conflicts.            | Real-time updates (e.g., collaborative editing).   | Data convergence in distributed databases.               |

If you just want to know how to deal with write conflicts, your options are:

1. avoid them by using the same leader for the same key
2. last write wins
3. Store siblings, and have a user resolve
4. Have the database eventually converge on a value via CRDTs or something like that

## Leaderless Replication

-> Write to many nodes
-> Read from many nodes

Where is used?
-> Cassandra
-> Riak

### Read repair

What value we read? 21 > 20 - bigger in terms of versioning. Correct the node which returned the smaller version.

### Anti entropy

Propagate changes between nodes in the background. In a single-leader or multi-leader we would use the replication log.

- only want to send some writes, other are already available

Here we use Merkle trees: to determine how two database tables differ really quickly and efficiently.

Merkle tree:
a:10 -> h(10)=358
=> h(358, 452)=321
b: 6 -> h(6) =452  
 => h(321, 509)=041
c: 2 -> h(2) =987
=> h(987, 762)=509
d: 4 -> h(4) =762

Compare merkle trees between nodes.
O(logN) time complexity

### Quorums

Instant reads of writes.

- cluster of N nodes
- write to W nodes
- read from R nodes
- Quorum is when W+R > N

Are quorums strongly consistent? No
Wll all users that perform a read at the exact same time get the same data? No.

Issues:

- write conflicts
- failed writes
- sloppy quorums (need for hinted handoff)

## Replication Summary

- > 1 DBs nodes
- potentially reading from many nodes or writing to many nodes

What do we gain?

1. Durability
2. Availability
3. Reducing Latency - Geographically spread - speed up
4. Increasing Throughput - With a single database server, there is a maximum threshold of concurrent reads and writes it can handle before performance degrades. By replicating to multiple servers, application requests can be distributed across replicas. More replicas means more capacity to handle load in parallel.

### Single leader replication

- \+ no write conflicts
- \- low write throughput
- \- single point of failure

### Multi-Leader replication

- \+ high write throughput
- \+ good for large geographical area
- \- write conflicts: version vectors: storing siblings or CRDTs

### Leaderless replication

Writing to many nodes at a time.
Reading from many nodes - checking highest version number
Quorum: W + R > N
Read repair
Anti-entropy Merkle tree

- \+ relatively high write throughput
- \+ quorum read/writes
- \- high read latency
- \- write conflicts

### Replication Strategy Examples

Here are some example scenarios demonstrating how these factors can influence replication strategy selection in real-world systems:

#### Online Retail Application

Large product catalog makes database large and complex
Requires strong consistency for order processing
Deployed across multiple geographic regions
Mostly read operations for product browsing

Recommended strategy: Leader-follower replication to handle large data, ensure strong consistency, and distribute reads across regions.

#### Gaming Application

Player data is relatively simple
Highly sensitive to latency for good gameplay
Read and write heavy for game state updates
Operates within a region for low latency

Recommended strategy: Multi-leader replication for fast reads/writes in a single region

#### Ride Sharing Application

Medium complexity data
Requires eventual consistency for high availability
Write-heavy workloads for trip updates
Cost sensitive infrastructure

Recommended strategy: Leaderless replication for efficient writes. Conflict resolution provides eventual consistency at low infrastructure cost.

#### System Size and Complexity

The size and complexity of the system are important factors. Large and complex systems make replication more difficult. Synchronous replication can slow down response times when copying large amounts of data across nodes. Smaller, simpler systems may not face these issues. Complex data structures also pose challenges for conflict resolution. Some replication strategies handle complexity better than others. Additionally, more complex systems may require more intricate monitoring and conflict-resolution mechanisms.

#### Consistency Needs

How much consistency does the application require? Applications demanding strong consistency may need synchronous replication to ensure replicas are synchronized. However, this impacts performance and availability. Applications tolerating some inconsistency can use asynchronous replication for better response times and availability despite replica lag.

#### Geographic Distribution

Consider geographic distribution and its impact on network latency. Systems spanning multiple regions struggle with synchronous replication's latency demands. Leaderless and multi-leader replication better tolerate network delays across global deployments. They maximize availability despite dispersed infrastructure. Furthermore, be aware that data replication across international boundaries may be subject to different data protection regulations.

#### Read/Write Workloads

Workload nature influences replication choice. Read-heavy systems suit leader-follower replication. Read requests can be distributed across follower replicas to balance load and improve response times. Write-heavy systems are better served by multi-leader or leaderless replication where writes are parallelized.

#### Replication Factor

The replication factor balances cost and durability. Higher factors increase resilience through more copies but also raise storage and management overhead. A factor of 3 is typical for good availability without excessive overhead, although the optimal factor can vary based on specific system requirements..

#### Consistency Models

So far we have focused on strong and eventual consistency models. But there are other consistency models that provide different guarantees and have implications for replication strategies.

Linearizability provides very strong ordering guarantees, ensuring reads instantly reflect the latest writes. This necessitates synchronous replication to keep replicas synchronized.

Sequential consistency guarantees ordering of writes across nodes, but allows some lag in propagating writes before reads. This enables some asynchronous replication flexibility.

Causal consistency only enforces order between related writes. Unrelated writes can be seen out of order. This further relaxes synchronicity needs for asynchronous replication.

These stronger models add ordering constraints that limit how asynchronous replication can be used. Weaker consistency models provide more flexibility but increase the risk of stale reads. Understanding these trade-offs helps guide the choice of replication strategy.

The flexibility of asynchronous replication comes at the cost of replication lag between leaders and followers. This lag can lead to a number of consistency issues that must be considered.

# Sharding

Sharding is a technique that addresses the challenges of horizontal database scaling. It involves partitioning the database into smaller, more manageable units called shards.

Despite the differences in terminology, the underlying concept remains the same: dividing the data into smaller, manageable units to improve query performance and scalability.

- Improved performance
- Availability
- Scalability

How does it work?
We need to break up our data.

## Types of sharding

### Range-based sharding

Pros: similar keys on the same node - good locality for range queries
Cons: hot spots

### Key-based sharding

Hash-range based sharding
Pros: Relatively even distribution of keys so less hot spots
Cons: No data locality for range queries

### Directory-based sharding

Directory-based sharding is an approach that relies on a lookup table to determine the distribution of records across shards.

## Factors to Consider When Selecting a Shard Key

Cardinality - To maximize the benefit of horizontal scaling, it is generally recommended to select a shard key with high cardinality.

Frequency - If a significant portion of the records contains only a subset of the possible shard key values, the shard responsible for storing that subset may become a hotspot.

Monotonic Change - If a shard key is based on a value that increases or decreases monotonically, it can result in unbalanced shards.

## Rebalancing the Shards

Shard rebalancing aims to achieve several key goals:

- Fair Load Distribution: After the rebalancing process, the workload should be evenly distributed among the nodes in the cluster.
- Minimal Disruption: The database should continue accepting read and write operations during the rebalancing process.
- Efficient Data Movement: The amount of data moved between nodes should be kept to a minimum.

- Fixed Number of Shards

  - If the shards are too large, rebalancing and recovery from node failures can become time-consuming and resource-intensive.
  - On the other hand, if the shards are too small, there is an increased overhead in maintaining and managing them.

- Dynamic Shards
  - One key advantage of dynamic sharding is its flexibility. It can be applied to both range-based sharding and hash-based sharding strategies.

## Request Routing in a Sharded Database

After sharding the dataset, the most critical consideration is determining how a client knows which node to connect to for an incoming request.

This problem becomes challenging because shards can be rebalanced, and the assignment of shards to nodes can change dynamically.

There are three main approaches to address this challenge:

1. Shard-Aware Node: In this approach, the clients can contact any node using a round-robin load balancer. If the contacted node owns the shard relevant to the request, it can handle the request directly. Otherwise, it forwards the request to the appropriate shard and routes the response back to the client.

2. Routing Tier: With this approach, client requests are sent to a dedicated routing tier that determines the node responsible for handling each request. The routing tier forwards the request to the appropriate node and returns the response to the client. The application communicates with the routing tier, not the nodes directly.

3. Shard-Aware Client: In this approach, clients are aware of the shard distribution across nodes. The client first contacts a configuration server to obtain the current shard-to-node mapping. Using this knowledge, the clients can then directly connect to the appropriate node for each request.

## Secondary Indexes

--- secondary indexes:
https://www.dynamodbguide.com/secondary-indexes

### Local secondary indexes

### Global secondary indexes

## Distributed transaction - Two phase commit

Why do we need it? Distributed transactions.
-> We need atomicity

When data needs to be atomically stored on multiple cluster nodes, nodes cannot make the data accessible to clients until the decision of other cluster nodes is known. Each node needs to know if other nodes successfully stored the data or if they failed.

1. Cross partition writes
2. Global Secondary indexes

The essence of two-phase commit, unsurprisingly, is that it carries out an update in two phases:

1. The prepare phase asks each node if it can promise to carry out the update.
2. The commit phase actually carries it out.

As part of the prepare phase, each node participating in the transaction acquires whatever it needs to assure that it will be able to do the commit in the second phase—for example, any locks that are required. Once each node is able to ensure it can commit in the second phase, it lets the coordinator know, promising the coordinator that it can and will commit in the second phase. If any node is unable to make that promise, then the coordinator tells all nodes to roll back, releasing any locks they have, and the transaction is aborted. Only if all the participants agree to go ahead does the second phase commence—at which point it's expected they will all successfully update. It is crucial for each participant to ensure the durability of their decisions using pattern like Write-Ahead Log. This means that even if a node crashes and subsequently restarts, it should be capable of completing the protocol without any issues.

Problems with 2PC:

- too many points of failure
  - coordinator can go down - no transactions can proceed, receiving nodes hold locks and can't touch rows
  - receiver goes down - transaction can't commit, coordinator needs to send it messages forever until it comes back up.

Conclusion:

- distributed transactions are hard and slow
- where possible be smart about how you partition your data to avoid them

## Linearizability

Or how to build linearizable storage? Why would we want so?
Linearizable storage will allow us to build apps on top of it, like:

- distributed locking
- service discovery

What is linearizable storage?

- we need this for correct reads
- linearizable - writes are ordered
  "Just one person with a lock"
  "Just one leader"

All writes are ordered.

> When we read from a linearizable storage our reads can never go back in time.

How do we order our writes?

- single leader replication: Replication log
- multi-leader replication: Version vectors/Lamport clocks

version vectors take O(n) space. they can tell us if writes are concurrent

lamport clocks take O(1) space. On a write, clock number is set to max(client, server) + 1

Sort by counter first and then by node. Lamport clocks only give us a total ordering.

We need "Total order" broadcast:

1. Every node has to agree on the order of writes
2. In the case of faults, we cannot lose any writes
   => distributed consensus

### RAFT - Distributed consensus

Protocol for implementing distributed consensus.
We store the operation like: term and epoch number

- log (log replication, leader election)
- state machine - takes input command from its log
- random timeout

RAFT:
https://thesecretlivesofdata.com/raft/

- RAFT creates fault tolerant, linearizable storage
- RAFT is slow - single leader
- RAFT is fault tolerant but it doesn't replace 2PC since all writes to replicas are the same

RAFT is a consensus algorithm used in distributed systems to ensure that multiple replicas of data remain consistent, even in the case of faults (e.g., network partitions, server crashes). It helps in maintaining a reliable and fault-tolerant state machine across a distributed system.

2PC (Two-Phase Commit) is a protocol used in distributed transactions to ensure atomicity, meaning that all involved nodes either commit or abort a transaction to maintain consistency. 2PC ensures that a transaction is either fully committed across all nodes or rolled back entirely, even in case of failures.

All Writes to Replicas Are the Same: In RAFT, once a log entry is committed, it is replicated to all the replicas. However, RAFT only ensures that the logs are consistent across replicas—it doesn’t care about the semantics of the actual data being written. RAFT ensures consistency at the log level, not at the transactional level.

### Leader election

A node is in state candidate.

- can't elect two leaders due to quorums
- old leaders can't code back due to fancing token
- leader has up to date log and can backfill

### Broadcasting writes

Writes backfill logs

1. there is only one leader per term
2. successful writes must make log fully up to date

Meaning: If two logs have the same term number at the same index they must be identical prior to that index

prefix <- suffix ->
log

## Coordination services

Thin layers built on top of distributed consensus algorithm.

Consensus is slow.

> ZooKeeper, etcd

A coordination service is a key-value store that allows us to store the data in a reliable way.

# Relational vs Non-relational

Relational: relationships, normalized data
We care about how data is organized

- bad data locality can lead to distributed transactions
- 2PC is slow
- reads from many nodes are slow

NoSQL DBs are denormalized data
-> better data locality but now we have repeated data

Non relational DBs

- avoid cross-partition reads, all relevant info stored together
- denormalized data leads to more writes, may need distributed transactions
- may have to send whole document over network depending on implementation

Conclusion: Non relational DBs are better for highly decoupled non relational data.

Top 10:

1. online file sharing system
2. url shortening
3. social media fb / twitter
4. online messaging app
5. webcrawer
6. news feed system for social media
7. trending topic system
8. CDN
9. web analytics tool
10. online ads platform

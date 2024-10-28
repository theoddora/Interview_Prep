# Back-of-the-Envelope Math

## What is the Purpose?
One of the purposes of back-of-the-envelope math is to justify a design. 

## Types of Back-of-the-Envelope Calculations
> **QPD (Query per day)** =
[Daily active users] x
[% of active users making the query] x
[Average number of queries made by each user per day] x
[Scaling factor]

Query per second (QPS) ~= QPD / 100k

There are 84,600 (24 x 60 x 60) seconds per day, you can round
that up to 100k for easier calculation.

When you divide by 100k, just remove 5 from the power of 10.
For example:
10^11 / 100k = 10^11-5 = 10^6

Daily active users
 : The daily active user count is something that you should ask the interviewer.
Sometimes they may tell you the number of users instead of active users. In that
case, you assume a percentage of total users to be active users.

% of Active Users Making the Query
 : Sometimes not all active users will perform a specific action. For example, if the
interviewer asks you to calculate the QPS for News Feed posts for Facebook,
you should assume only a fraction of the users will post since most are just News
Feed readers. Usually, 1% - 20% writer to reader is a fair assumption, depending
on the application.

Average Number of Queries Made by Each User Per Day
 : You should make an assumption of how many requests an active user makes
each day.

Scaling Factor
 : Give a product scenario to show good product sense. For example, when
requesting a ridesharing service, mention how weekend nights have more
activity and that you’ll assume it has 5-10 times the average traffic. The purpose is to demonstrate to the interviewer that you have thought
about a potential bottleneck.

> **Storage capacity for time horizon** =
[Daily active users] x
[% of active users making the query to persist] x
[Average number of queries made by each user] x
[Data size per query] x
[Replication factor] x
[Time horizon]

Data Size per Query
 : Make sure you consider all the data you’re storing. If you’re saving an Instagram
post, make sure you remember to calculate both the photo and the post metadata.

Replication Factor
 : Generally, companies replicate a database into other databases for backup.
Typically that number is 3. The point is to show the interviewer you have
thought about it.

Time Horizon
 : You need to know the time horizon to plan for capacity. Usually, somewhere
between 1-5 years should be fine. In practice, capacity planning is very
contextual.

To solve for the total memory:
1. Convert All Numbers to Scientific Number
2. Group all the 10s together 
3. Group all other numbers together
4. Find out the final number
5. Convert the final number into a readable number
6. Do something with that number

# API Design
Ultimately, your
goal is to ensure the API is clear, efficient, and solves the problem at hand. Here
are some advanced concepts to talk about during the API design:

## Idempotency
1. Use Unique Identifiers for Requests.
Assign a unique ID (e.g., UUID) to each request, which the server uses to track and process only once. This can also be the "\<User-Id>+\<method-name>+\<UUID>"
2. Use Conditional Logic in Requests: For an update request (PUT), a client might specify an If-Match header with the resource’s current version. If the resource has changed, the server does not perform the update.
3. Implement Retries with Idempotent Operations - For operations where retries are necessary (e.g., network errors), design operations to be inherently idempotent (e.g., PUT and DELETE requests in REST). In a payment API, mark transactions as “processed” after the first successful charge. Subsequent attempts detect this status and avoid re-charging the customer.
4. Store and Check Operation Results Before Performing the Operation - Cache or record results of completed actions and check this record before executing the operation.
5. Leverage HTTP Methods with Defined Idempotency - Use HTTP methods that are idempotent by definition (GET, PUT, DELETE, HEAD, and OPTIONS).

## Client vs Server Generated Data
You can have the server generate the timestamp instead of the
client.

## Efficiency
You should think
about pagination.

## Correctness
API signature is true
to its task, and the input and output are sufficient to satisfy the question’s
requirements.

## Focus on the Core
For a given API, focus on the input, output, and signature name. Don’t focus on
a protobuf and RESTul schema since that’s not the core of the question and is
pretty wasteful. Only focus on it if the interviewer directly asks for RESTful
design.

## REST vs RPC vs GraphQL
### REST (Representational State Transfer)
REST is an architectural style for designing networked applications. It uses HTTP methods (GET, POST, PUT, DELETE) to operate on resources, which are typically represented by URLs.

Each URL represents a resource, and HTTP methods define operations on that resource.

REST is stateless, scalable, and leverages caching and HTTP standards, making it suitable for CRUD operations.

REST APIs may become complex with multiple endpoints for different resource actions, which can be inefficient for complex, client-driven requests.

**Interview**: Understand HTTP methods and their idempotency (GET, PUT, DELETE).
Know the benefits and limitations of RESTful design, especially for CRUD operations.
Be familiar with RESTful principles, resource naming conventions, and HTTP status codes.

### RPC (Remote Procedure Call)
RPC is a protocol or design that allows a client to directly call methods (functions or procedures) on a remote server, appearing as local function calls.

Each API endpoint represents a method or action rather than a resource.

RPC can be very efficient for complex operations, as it allows multiple actions within a single call.

Enforcing statelessness and idempotency can be difficult; stateful calls require additional tracking and error handling.

**Interview**: Explain the difference between function-based and resource-based API designs.
Discuss idempotency and how to handle it for repeated RPC calls.
Be aware of the different types of RPC implementations (e.g., JSON-RPC, XML-RPC, gRPC) and when each is ideal.

### GraphQL
GraphQL is a query language for APIs that allows clients to specify exactly the data they need, retrieving multiple resources in one request.

Single endpoint (often /graphql) where queries and mutations are defined, allowing for specific data retrieval without over-fetching.

Client flexibility to request only the needed data, which can reduce payload size and increase efficiency.

Complex queries may increase server load and require careful control over data access to prevent performance issues and protect sensitive data.

**Interview**: Understand the query language, including queries, mutations, and subscriptions.
Be able to explain advantages (e.g., flexible data fetching) and potential pitfalls (e.g., performance and complexity).
Know about schema definitions, resolver functions, and how GraphQL can be optimized for efficiency and security.

### Comparison Table
| **Aspect**            | **REST**                                                                                 | **RPC**                                                                                              | **GraphQL**                                                                                          |
|-----------------------|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|
| **Endpoint Structure**| Multiple endpoints represent resources, e.g., `/users`, `/posts`.                        | Multiple endpoints represent actions or methods, e.g., `/getUser`, `/createOrder`.                   | Single endpoint, typically `/graphql`, supports complex queries and mutations.                       |
| **Data Fetching**     | Retrieves full resources (often over-fetches data).                                      | Retrieves data based on the specific action but can be rigid in structure.                           | Allows clients to specify exactly what data is needed, reducing over-fetching.                       |
| **Request Type**      | HTTP-based with standardized methods (GET, POST, PUT, DELETE).                           | Function call-based, usually with HTTP or other protocols like gRPC.                                 | Query language with a single endpoint and methods for queries and mutations.                         |
| **Use Case**          | CRUD operations, straightforward resource-based services.                                | Services with complex logic, where specific functions are more efficient than resource-based models. | Client-driven APIs where flexible, specific data requests are required across multiple resources.    |
| **Complexity**        | Can be cumbersome with deeply nested or complex relationships, often requiring multiple requests. | Simpler logic but requires detailed idempotency and tracking for complex state.                       | Reduces request complexity by fetching complex data in a single call, though server complexity may increase. |
| **Caching**           | HTTP caching is inherent (GET requests), making REST APIs highly cacheable.              | Limited caching; often requires custom caching solutions.                                            | Caching is complex as queries are dynamic and may require custom caching logic at the resolver level.|
| **Learning Curve**    | Moderate; leverages familiar HTTP methods and URLs.                                      | Low to moderate; can be easier to learn if already familiar with function-based programming.         | High; requires understanding of query language, schema, resolvers, and error handling.               |


### Other Methods to Define an API

#### gRPC (Google Remote Procedure Call):
Description: gRPC is an open-source RPC framework that uses HTTP/2 for transport, Protocol Buffers (protobufs) for data serialization, and can operate over multiple programming languages.
Best For: High-performance, low-latency applications, especially for inter-service communication in microservices architectures.
Strength: Supports bi-directional streaming, efficient serialization, and strongly typed requests.

Note: Understand the high-performance benefits and be able to discuss HTTP/2 and Protocol Buffers.
Know about unary and streaming calls (client-side, server-side, bi-directional).
Be familiar with use cases, especially in microservices, where low latency and high throughput are critical.

#### WebSockets:
Description: WebSockets provide a persistent connection allowing real-time, bi-directional communication between client and server.
Best For: Applications requiring real-time updates, like chat apps or live data feeds.
Strength: Low-latency updates due to the persistent connection, reducing request overhead.

# Schema design
During the system design interview, it’s critical to have clarity of the schema.
Come up with a
logical schema first and ensure the integrity and the relationships are clear and
how the APIs will fetch the information.

## Defining Schemas
A table should have a primary key that uniquely identifies a row. The primary key can also be a clustered index which means you can
fetch a primary key efficiently. Other tables can use the primary key as a foreign
key (FK). A table has columns to store row-level information.

1. Step 1: Create the Tables Needed
2. Step 2: Relationships.
3. Step 3: Many-To-Many relationships

## Normalization vs Denormalization

Some people get stuck debating if they should normalize tables or keep them
denormalized because of the inefficiency of the join. Normalization doesn’t
matter that much in an interview setting since it’s a generic debate that’s usually
not unique to the interview question. However, it might be worth bringing up if
you identify the read throughput to be an issue.

## Indexing Strategies
When you’re designing the schema, you need to think about the efficiency of
your query with your proposed schema. Without proper indexing, it may result in
a full table scan. In a system design interview, it’s worth mentioning how you
would index to achieve better performance.

### What is Indexing?
Abstractly, an index is just a sorted table that allows the search to be O(Log N)
using binary searching with a sorted data structure. Internally, an index can be
implemented using B-Tree or LSM, which uses Sorted Strings Table (SST).

### Primary Index
When the main table is created, by default, the primary key is also the clustered
index which means the primary key on disk sorts the main table itself. Therefore,
searching by the primary key will be efficient.

### Secondary Index
You may want to consider adding in a secondary index which is another
sorted table to reference the main table record. The advantage is a quick
reference to the record of interest, and the disadvantage is the write will be
slower with more tables to update. Having additional indexes is still preferable
for higher read-to-write ratio applications.

### Index Use Cases

* Key or attribute lookup
* Range Lookup
* Prefix Search

### Composite Index
This section will talk
about indexing on multiple columns and requires a bit more thinking on top of
just throwing an index to a column. The idea is the same for row key design for
NoSQL design, where NoSQL concatenates the key instead of defining it as
separate columns.

### Geo Index
The world geodatabase is complicated with alternatives like R-Tree, kd-tree,
2dsphere, Google S2, etc. 

If you wish to go to disk, here are two simplistic options that are good enough
for an interview:
1. Option - Geohash solution like in the prefix search section.
2. Option - Reverse index of location_id to a list of objects like drivers or points
of interest.

location_id → [object]

You can represent location_id as a tuple (longitude, latitude). Then, you can
calculate the values using the floored longitude and latitude. That way, you don’t
need separate storage to store longitude and latitude ranges to a grid ID. For
example, (1.11, 2.25) can be floored to the (1, 2) grid and use (1,2) as an ID to a
location block.

## Databases

Definition
 : A database is an organized collection of data that is stored by the application for
durability.

### How Do I Choose a Database?
**CAP theorem** is a generalized term to help understand distributed databases.
* C stands for consistency, which means all the databases see the same data at
the same time. This means users can read or write from/to any node in the system and will receive the same data. It is equivalent to having a single up-to-date copy of the data.
* A stands for availability, which means the database is up to serve traffic. Availability means every request received by a non-failing node in the system must result in a response. Even when severe network failures occur, every request must terminate. In simple terms, availability refers to a system’s ability to remain accessible even if one or more nodes in the system go down.
* P stands for partition tolerance, which means the system continues to work if
there’s a network issue between databases. A partition is a communication break (or a network failure) between any two nodes in the system, i.e., both nodes are up but cannot communicate with each other. A partition-tolerant system continues to operate even if there are partitions in the system. Such a system can sustain any network failure that does not result in the failure of the entire network. Data is sufficiently replicated across combinations of nodes and networks to keep the system up through intermittent outages.

CAP theorem states you can only have two of the three.
* AC: Means there’s no partition with a single machine.
* CP: Means if there’s a network issue between the databases, the request fails in
favor of consistency.
* AP: Means if there’s a network issue between the databases, the request
continues to work in favor of availability.

The best way
to choose a database is to understand a list of categories of databases and what
they are good at. 

### Types of Databases

#### Relational Database
**When to Use?**
In relational databases, it is easy to represent the entities as tables and define the
relationship between them. It supports transactions to write to one or many
entities and supports simple to complex read queries. Y ou’re able to add in an
ad-hoc index to improve the read performance at the expense of write
performance. Also, if you have multiple entities with shared attributes, you can
fetch results with a joined or unioned table. Also, it supports updates for a record
well. Some databases are append-only.

***Advanced Concepts***

Most traditional relational databases use B-Tree based indexing, which is better
for reads and less good for writes.

Relational databases can provide stronger data integrity through transaction
guarantee by enforcing constraint through entities through foreign keys.

***ACID***

* Atomicity
 : The writes in a transaction are executed all at once and cannot be broken into smaller
parts. If there are faults when executing the transaction, the writes in the transaction
are rolled back. So atomicity means “all or nothing”. Transaction management systems often use logging mechanisms to enable this rollback feature. 
* Consistency
 : Unlike “consistency” in CAP theorem, which means every read receives the most recent write or an error, here consistency means preserving database invariants. Any data
written by a transaction must be valid according to all defined rules and maintain the
database in a *good state*. It checks for constrint violations during transactions.
* Isolation
 : When there are concurrent writes from two different transactions, the two transactions
are isolated from each other. The most strict isolation is “serializability”, where each
transaction acts like it is the only transaction running in the database. However, this is
hard to implement in reality, so we often adopt a loser isolation level.

![ ](/Resources/images/isolation.png)

* Durability
 : Data is persisted after a transaction is committed even in a system failure. In a
distributed system, this means the data is replicated to some other nodes.
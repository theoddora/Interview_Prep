# Glossary

## IPC

Communication between processes over the network, or inter-
process communication (IPC)

## Distributed system

We are concerned with backend applications that run
on commodity machines and implement some kind of business
service. A distributed system is a group of
machines that communicate over network links. However, from a
run-time point of view, a distributed system is a group of software
processes that communicate via inter-process communication (IPC)
mechanisms like HTTP. And from an implementation perspective,
a distributed system is a group of loosely-coupled components
(services) that communicate via APIs.

## Service

A service implements one specific part of the overall system’s capabilities. At the core of a service sits the business logic, which
exposes interfaces to communicate with the outside world.

## Adapters

Adapters
are needed to connect IPC mechanisms to service interfaces.

### Inbound

An
inbound adapter is part of the service’s Application Programming
Interface (API); it handles the requests received from an IPC mechanism, like HTTP, by invoking operations defined in the service
interfaces.

### Outbound

Outbound adapters grant the business logic
access to external services, like data stores.

## Server

A process running a service

## Client

A process sending requests to a server

## Overhead

In computing, overhead refers to the additional resources or costs required to perform a task beyond the minimum needed to accomplish the task itself. It represents the "extra work" the system does to manage, support, or facilitate operations.

**Data Freshness**:

1. Real-Time
   : A stock trader sitting at home needs the data to be real-time because a delay in
   the price feed may cause the trader to make the wrong trading decision.
2. Near Real-Time
   : When a celebrity is streaming their experience at a baseball game on Facebook
   Live, the stream itself should be near real-time, but a couple of seconds delay
   is acceptable. The users won’t feel a difference with a couple of seconds delay,
   but if the stream is delayed by a couple of hours, some users will likely find
   out because the game is already over.
3. Batch Process
   : Because real-time and near real-time systems are challenging and expensive to
   build, some applications can still have a good user experience even if it takes a
   couple of hours or days to run. For example, a static website’s web crawler for
   search does not need to be updated often.

**Durability**
: Durability is a fundamental property of database systems and distributed systems, particularly in the context of data management and transaction processing. It ensures that once a transaction has been committed, its effects are permanent and will survive any subsequent failures, such as crashes or power outages.

1. High Durability
   : When you’re storing users’ life photos, it is extremely important to be highly
   durable. Losing a photo would mean never being able to see that moment of
   their life again. So, in the interview, you should emphasize the importance of
   durability design to prevent correlated failures.
2. Medium Durability
   : For casual chats that happened years ago, you might argue that the users will
   rarely look at the ancient chat history again. While the chat history is still
   important to be durable, losing a message that happened years ago wouldn’t
   get a user super angry
3. Low Durability
   : For a rich sharing service to capture drivers’ location, it is acceptable if we lose
   a driver’s location for a moment in time because we will get their location for
   their next update in the next few seconds. So losing location data wouldn’t
   result in many impacts on the underlying system.

**Idempotency**
: An API call or operation is idempotent if it has the same result no matter how many times it's applied

## Bandwidth

In computer networking, bandwidth refers to the amount of data a network can transmit over a connection in a given amount of time. So just like a co-worker might only have the bandwidth for a certain number of projects, a network only has bandwidth for a limited amount of data. Typically, bandwidth is represented in the number of bits, kilobits, megabits or gigabits that can be transmitted in 1 second. Synonymous with capacity, bandwidth describes data transfer rate. Bandwidth is not a measure of network speed -- a common misconception.

## Fault tolerance

Fault tolerance is the ability of a system to continue operating properly even when some of its components fail. It involves building systems with redundancy and mechanisms that allow for graceful handling of faults or errors, minimizing downtime and preventing complete failure. Fault tolerance is essential for critical applications where uptime and reliability are crucial, such as in finance, healthcare, telecommunications, and cloud services.

## Availability

Availability (also known as service availability) is both a commonly used metric to quantitatively measure resiliency, as well as a target resiliency objective.

> Availability is the percentage of time that a workload is available for use.

Available for use means that it performs its agreed function successfully when required.

This percentage is calculated over a period of time, such as a month, year, or trailing three years. Applying the strictest possible interpretation, availability is reduced anytime that the application isn’t operating normally, including both scheduled and unscheduled interruptions. We define availability as follows:

Availability = (available for use time) / (total time)

- Availability is a percentage uptime (such as 99.9%) over a period of time (commonly a month or year)
- Common short-hand refers only to the “number of nines”; for example, “five nines” translates to being 99.999% available

| **Availability** | **Maximum Unavailability (per year)** | **Application Categories**                                 |
| ---------------- | ------------------------------------- | ---------------------------------------------------------- |
| 99%              | 3 days 15 hours                       | Batch processing, data extraction, transfer, and load jobs |
| 99.9%            | 8 hours 45 minutes                    | Internal tools like knowledge management, project tracking |
| 99.95%           | 4 hours 22 minutes                    | Online commerce, point of sale                             |
| 99.99%           | 52 minutes                            | Video delivery, broadcast workloads                        |
| 99.999%          | 5 minutes                             | ATM transactions, telecommunications workloads             |

Measuring availability based on requests. For your service it may be easier to count successful and failed requests instead of “time available for use”. In this case the following calculation can be used:

Availability = (Successful responses) / (Valid requests)

This is often measured for one-minute or five-minute periods. Then a monthly uptime percentage (time-base availability measurement) can be calculated from the average of these periods. If no requests are received in a given period it is counted at 100% available for that time.

**Calculating availability with hard dependencies.** Many systems have hard dependencies on other systems, where an interruption in a dependent system directly translates to an interruption of the invoking system. This is opposed to a soft dependency, where a failure of the dependent system is compensated for in the application. Where such hard dependencies occur, the invoking system’s availability is the product of the dependent systems’ availabilities. For example, if you have a system designed for 99.99% availability that has a hard dependency on two other independent systems that each are designed for 99.99% availability, the workload can theoretically achieve 99.97% availability:

Availinvok × Availdep1 × Availdep2 = Availworkload

99.99% × 99.99% × 99.99% = 99.97%

It’s therefore important to understand your dependencies and their availability design goals as you calculate your own.

## Latency

> Response Time = Latency + Processing Time

**Response Time**: The time difference between the client sending the request and
receiving the response.

**Latency**: The time the request has to wait before it is processed.

**Processing Time**: The time it takes to process the request

**Throughput**: The number of requests processed per second by
the application. In short, throughput is about maximizing how much work a system can complete within a set period, and it's crucial for systems that need to handle large volumes of data or transactions, such as online services, high-traffic websites, and streaming platforms.

| **System**             | **Throughput Measure**        | **Example**                   |
| ---------------------- | ----------------------------- | ----------------------------- |
| Web Server             | Requests per second (RPS)     | 10,000 requests per second    |
| Database               | Transactions per second (TPS) | 1,500 transactions per second |
| Network                | Bits per second (bps)         | 500 Mbps                      |
| Data Processing System | Records per hour              | 100 million records per hour  |
| Message Queue          | Messages per second           | 50,000 messages per second    |

The amount of data an application can write to stable storage on the server over a period of time is a measurement of the write throughput of a distributed system. Write throughput is therefore an important aspect of performance.

In short, latency is about how fast a system responds, while availability is about how reliably a system stays up and accessible. A system can be highly available (always accessible) but have high latency (slow response), or it could have low latency (quick response) but low availability (frequent downtime). Balancing both is crucial for many applications.

| **Aspect**            | **Latency**                                      | **Availability**                                         |
| --------------------- | ------------------------------------------------ | -------------------------------------------------------- |
| **What it measures**  | Time delay for processing requests               | Percentage of uptime over a given period                 |
| **Focus**             | Speed and responsiveness                         | Reliability and uptime                                   |
| **Example Metric**    | Milliseconds for a round-trip request            | Percentage (e.g., 99.99%) of operational time            |
| **Priority for**      | Real-time applications (e.g., gaming, streaming) | High-demand applications (e.g., banking, cloud services) |
| **Optimization Goal** | Reducing response time                           | Increasing uptime and handling failures gracefully       |

![ ](/Resources/images/throughput.jpeg)

## (CIA) triad

The CIA triad is a fundamental model in information security, representing the three core principles that guide efforts to protect data and systems. Each letter in "CIA" stands for a distinct principle:

### Availability

Ensures that information and systems are accessible to authorized users when needed.

Techniques:

- Redundant Systems: Uses multiple backup systems to ensure that resources are available even if one system fails (e.g., multiple servers, data centers).
- Load Balancing: Distributes workloads across multiple systems to prevent overloading and maintain smooth performance.
- Backup and Recovery: Creates and maintains copies of data so it can be restored if lost (e.g., periodic data backups, disaster recovery plans).
- DDoS Protection: Mitigates Distributed Denial of Service attacks that aim to make services unavailable by overwhelming them with requests.
- Regular Maintenance and Patching: Ensures systems are up-to-date and secure, reducing the risk of downtime due to vulnerabilities.

### Confidentiality

Sensitive information is kept private and only accessible to authorized individuals or systems. Encryption is a common technique used to achieve confidentiality by ensuring data in a way that makes it unreadable to unauthorized parties.

Technique:

- Encryption: Converts data into a coded format (e.g., AES, RSA) that can only be read by authorized parties.
- Access Controls: Implements restrictions to ensure only authorized users can access specific data (e.g., role-based access control or attribute-based access control).
- Authentication: Verifies the identity of users (e.g., passwords, multi-factor authentication, biometric verification).
- Data Masking: Obscures sensitive information to limit its visibility (e.g., showing only the last four digits of a credit card number).
- Steganography: Hides data within other files (like images) to avoid detection.

### Integrity

Protects data from unauthorized modifications or tampering, ensuring its accuracy and reliability. Mechanisms like hashing, digital signatures, and checksums are used to verify that information remains consistent and unaltered from its original form.

Technique:

- Hashing: Generates a unique hash for data (e.g., SHA-256) so that any change in the data can be detected.
- Digital Signatures: Provides a way to verify the authenticity and integrity of messages or documents, often used in combination with public-key encryption.
- Checksums: Creates a small block of data based on file contents to detect accidental or intentional modifications.
- Message Authentication Codes (MACs): Uses cryptographic hashing and a secret key to verify data integrity and authenticity.
- Version Control: Tracks changes to files over time to prevent accidental data loss or unauthorized alterations (e.g., Git for codebases).

# Consistency models

https://jepsen.io/consistency/models#consistency-models

| Consistency Model                           | Description                                                                                   | Pros                                          | Cons                                               |
| ------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------- | -------------------------------------------------- |
| **Linearizability (Single-Copy Atomicity)** | Operations appear instantaneous with real-time ordering.                                      | Clear, consistent state                       | High latency in distributed systems                |
| **Strong Consistency**                      | Guarantees all clients see the latest write immediately.                                      | High accuracy, avoids conflicts               | High latency due to synchronization                |
| **Sequential Consistency**                  | All clients see operations in the same sequential order, though not necessarily in real-time. | Simpler, often faster than strong consistency | Some synchronization still required                |
| **Causal Consistency**                      | Maintains order of causally related operations; unrelated operations may be unordered.        | Good balance of consistency and availability  | Complex to implement                               |
| **Release Consistency**                     | Updates propagate on acquire/release synchronization points rather than immediately.          | Efficient with controlled synchronization     | More relaxed consistency outside critical sections |
| **Read-Your-Writes Consistency**            | Ensures a client’s reads reflect its own previous writes.                                     | Immediate feedback for interactive apps       | No guarantees for other clients                    |
| **Monotonic Read Consistency**              | Ensures clients do not read older versions after seeing newer ones.                           | Logical read progression                      | Requires version tracking                          |
| **Eventual Consistency**                    | Ensures all replicas converge to the same state eventually, but reads may be stale initially. | High availability, low latency                | Temporary inconsistency                            |

# What is a cluster?

a cluster is a group of interconnected computers, known as nodes or servers, that work together as a single system to accomplish tasks. Clusters provide enhanced performance, reliability, and scalability compared to single machines, and are widely used in data centers, cloud computing, and high-performance computing environments.

## Key Features of a Cluster

- Distributed Processing: Tasks are split across multiple nodes, allowing the system to handle larger workloads and process tasks faster.
- Redundancy and Fault Tolerance: Clusters often provide redundancy, so if one node fails, others can take over to keep the system running.
- Scalability: By adding more nodes, clusters can scale horizontally, handling more data and processing power without requiring bigger or more powerful individual machines.
- Load Balancing: Tasks are distributed across nodes, balancing the workload to prevent any single node from being overwhelmed.
- Shared Storage: Nodes may access shared storage resources, or each node might have its own local storage with data replicated across the cluster.

## Types of Clusters

- High-Availability (HA) Clusters: Designed to minimize downtime. If one node fails, another takes over to ensure continuous service. Common in mission-critical applications.
- Load-Balancing Clusters: Distribute incoming requests across nodes to evenly share the workload. Often used in web servers and other applications where large numbers of requests are processed.
- High-Performance Computing (HPC) Clusters: Designed for compute-intensive tasks, such as scientific simulations and complex calculations. Typically involves powerful nodes working together to complete tasks in parallel.
- Big Data Clusters: Specialized for data processing tasks, often with frameworks like Hadoop or Spark, to analyze large datasets by distributing the data and processing across nodes.
- Storage Clusters: Used to manage large amounts of data with high availability and redundancy, common in cloud storage systems.

# Back-of-the-Envelope Math

## What is the Purpose?

One of the purposes of back-of-the-envelope math is to justify a design.

## Types of Back-of-the-Envelope Calculations

> **QPD (Query per day)** =
> [Daily active users] x
> [% of active users making the query] x
> [Average number of queries made by each user per day] x
> [Scaling factor]

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
> [Daily active users] x
> [% of active users making the query to persist] x
> [Average number of queries made by each user] x
> [Data size per query] x
> [Replication factor] x
> [Time horizon]

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

## Metrics

| **Prefix**     | **Bytes** or **Power of 1k** | **Unit**    |
| -------------- | ---------------------------- | ----------- |
| PB - petabytes | 10^15 or 5                   | Quadrillion |
| TB - terabytes | 10^12 or 4                   | Trillion    |
| GB - gigabytes | 10^9 or 3                    | Billion     |
| MB - megabytes | 10^6 or 2                    | Million     |
| kB - kilobytes | 10^3 or 1                    | Thousand    |

1 Byte = 8 bits

## Latency

### Latency Comparison Numbers (~2012)

| Operation                          | Time (ns)   | Time (us) | Time (ms) | Comparisons                 |
| ---------------------------------- | ----------- | --------- | --------- | --------------------------- |
| L1 cache reference                 | 0.5         |           |           |                             |
| Branch mispredict                  | 5           |           |           |                             |
| L2 cache reference                 | 7           |           |           | 14x L1 cache                |
| Mutex lock/unlock                  | 25          |           |           |                             |
| Main memory reference              | 100         |           |           | 20x L2 cache, 200x L1 cache |
| Compress 1K bytes with Zippy       | 3,000       | 3         |           |                             |
| Send 1K bytes over 1 Gbps network  | 10,000      | 10        |           |                             |
| SSD seek                           | 100,000     | 100       | 0.1       | ~1GB/sec SSD                |
| Read 4K randomly from SSD\*        | 150,000     | 150       |           | ~1GB/sec SSD                |
| Read 1 MB sequentially from memory | 250,000     | 250       | 0.25      |                             |
| Round trip within same datacenter  | 500,000     | 500       | 0.5       |                             |
| Read 1 MB sequentially from SSD\*  | 1,000,000   | 1,000     | 1         | ~1GB/sec SSD, 4X memory     |
| Disk seek                          | 10,000,000  | 10,000    | 10        | 20x datacenter roundtrip    |
| Read 1 MB sequentially from disk   | 20,000,000  | 20,000    | 20        | 80x memory, 20x SSD         |
| Send packet CA->Netherlands->CA    | 150,000,000 | 150,000   | 150       |                             |

## Notes

- 1 ns = 10^-9 seconds
- 1 us = 10^-6 seconds = 1,000 ns
- 1 ms = 10^-3 seconds = 1,000 us = 1,000,000 ns

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

| **Aspect**             | **REST**                                                                                          | **RPC**                                                                                              | **GraphQL**                                                                                                  |
| ---------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Endpoint Structure** | Multiple endpoints represent resources, e.g., `/users`, `/posts`.                                 | Multiple endpoints represent actions or methods, e.g., `/getUser`, `/createOrder`.                   | Single endpoint, typically `/graphql`, supports complex queries and mutations.                               |
| **Data Fetching**      | Retrieves full resources (often over-fetches data).                                               | Retrieves data based on the specific action but can be rigid in structure.                           | Allows clients to specify exactly what data is needed, reducing over-fetching.                               |
| **Request Type**       | HTTP-based with standardized methods (GET, POST, PUT, DELETE).                                    | Function call-based, usually with HTTP or other protocols like gRPC.                                 | Query language with a single endpoint and methods for queries and mutations.                                 |
| **Use Case**           | CRUD operations, straightforward resource-based services.                                         | Services with complex logic, where specific functions are more efficient than resource-based models. | Client-driven APIs where flexible, specific data requests are required across multiple resources.            |
| **Complexity**         | Can be cumbersome with deeply nested or complex relationships, often requiring multiple requests. | Simpler logic but requires detailed idempotency and tracking for complex state.                      | Reduces request complexity by fetching complex data in a single call, though server complexity may increase. |
| **Caching**            | HTTP caching is inherent (GET requests), making REST APIs highly cacheable.                       | Limited caching; often requires custom caching solutions.                                            | Caching is complex as queries are dynamic and may require custom caching logic at the resolver level.        |
| **Learning Curve**     | Moderate; leverages familiar HTTP methods and URLs.                                               | Low to moderate; can be easier to learn if already familiar with function-based programming.         | High; requires understanding of query language, schema, resolvers, and error handling.                       |

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

- Key or attribute lookup
- Range Lookup
- Prefix Search

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

- C stands for consistency, which means all the databases see the same data at
  the same time. This means users can read or write from/to any node in the system and will receive the same data. It is equivalent to having a single up-to-date copy of the data.
- A stands for availability, which means the database is up to serve traffic. Availability means every request received by a non-failing node in the system must result in a response. Even when severe network failures occur, every request must terminate. In simple terms, availability refers to a system’s ability to remain accessible even if one or more nodes in the system go down.
- P stands for partition tolerance, which means the system continues to work if
  there’s a network issue between databases. A partition is a communication break (or a network failure) between any two nodes in the system, i.e., both nodes are up but cannot communicate with each other. A partition-tolerant system continues to operate even if there are partitions in the system. Such a system can sustain any network failure that does not result in the failure of the entire network. Data is sufficiently replicated across combinations of nodes and networks to keep the system up through intermittent outages.

CAP theorem states you can only have two of the three.

- AC: Means there’s no partition with a single machine.
- CP: Means if there’s a network issue between the databases, the request fails in
  favor of consistency.
- AP: Means if there’s a network issue between the databases, the request
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

**_Advanced Concepts_**

Most traditional relational databases use B-Tree based indexing, which is better
for reads and less good for writes.

Relational databases can provide stronger data integrity through transaction
guarantee by enforcing constraint through entities through foreign keys.

**_ACID_**

- Atomicity
  : The writes in a transaction are executed all at once and cannot be broken into smaller
  parts. If there are faults when executing the transaction, the writes in the transaction
  are rolled back. So atomicity means “all or nothing”. Transaction management systems often use logging mechanisms to enable this rollback feature.
- Consistency
  : Unlike “consistency” in CAP theorem, which means every read receives the most recent write or an error, here consistency means preserving database invariants. Any data
  written by a transaction must be valid according to all defined rules and maintain the
  database in a _good state_. It checks for constrint violations during transactions.
- Isolation
  : When there are concurrent writes from two different transactions, the two transactions
  are isolated from each other. The most strict isolation is “serializability”, where each
  transaction acts like it is the only transaction running in the database. However, this is
  hard to implement in reality, so we often adopt a loser isolation level.

![ ](/Resources/images/isolation.png)

- Durability
  : Data is persisted after a transaction is committed even in a system failure. In a
  distributed system, this means the data is replicated to some other nodes.

# Computer science

## Hash functions

A hash function is a mathematical function that takes an input (or ‘message’) and returns a fixed-size string of bytes.

Searching for specific data within an array can be slow (at least O(log n) time). This is where hash tables come in. They are a specialized data structure designed for lightning-fast lookups. Unlike arrays, hash tables prioritize retrieval speed over insertion speed.

### Collision resolutions

- Open addressing
  - Linear probing
  - Plus 3 rehash
  - Quadratic probing (failed attempts)^2
  - Double hashing
- Closed addressing
  - Chaining addresses

### Summary

- Used to index large amounts of data
- Address of each key calculated using the key itself
- Collisions resolved with open or closed addressing
- Hashing is widely used in database indexing, compilers, caching, password authentication and more
- Insertion, deletion and retrieval occur in constant time

## Base 36

Base 36 is a positional number system that uses 36 different symbols to represent numbers.
Base 36 is used in different areas of computer science, such as URL shortening, cookie generation,
and encoding of large numbers. One interesting feature of Base 36 is that it allows us to represent
large numbers in a compact way, which is useful in web applications and databases.

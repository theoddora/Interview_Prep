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

* Availability is a percentage uptime (such as 99.9%) over a period of time (commonly a month or year)
* Common short-hand refers only to the “number of nines”; for example, “five nines” translates to being 99.999% available

| **Availability** | **Maximum Unavailability (per year)** | **Application Categories**                          |
|------------------|---------------------------------------|----------------------------------------------------|
| 99%              | 3 days 15 hours                      | Batch processing, data extraction, transfer, and load jobs |
| 99.9%            | 8 hours 45 minutes                   | Internal tools like knowledge management, project tracking |
| 99.95%           | 4 hours 22 minutes                   | Online commerce, point of sale                      |
| 99.99%           | 52 minutes                           | Video delivery, broadcast workloads                |
| 99.999%          | 5 minutes                            | ATM transactions, telecommunications workloads     |

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

| **System**              | **Throughput Measure**           | **Example**                                        |
|-------------------------|----------------------------------|----------------------------------------------------|
| Web Server              | Requests per second (RPS)       | 10,000 requests per second                         |
| Database                | Transactions per second (TPS)   | 1,500 transactions per second                      |
| Network                 | Bits per second (bps)           | 500 Mbps                                           |
| Data Processing System  | Records per hour                | 100 million records per hour                       |
| Message Queue           | Messages per second             | 50,000 messages per second                         |


In short, latency is about how fast a system responds, while availability is about how reliably a system stays up and accessible. A system can be highly available (always accessible) but have high latency (slow response), or it could have low latency (quick response) but low availability (frequent downtime). Balancing both is crucial for many applications.

| **Aspect**            | **Latency**                                 | **Availability**                                   |
|-----------------------|---------------------------------------------|----------------------------------------------------|
| **What it measures**  | Time delay for processing requests          | Percentage of uptime over a given period           |
| **Focus**             | Speed and responsiveness                    | Reliability and uptime                             |
| **Example Metric**    | Milliseconds for a round-trip request       | Percentage (e.g., 99.99%) of operational time      |
| **Priority for**      | Real-time applications (e.g., gaming, streaming) | High-demand applications (e.g., banking, cloud services) |
| **Optimization Goal** | Reducing response time                      | Increasing uptime and handling failures gracefully |



## (CIA) triad

The CIA triad is a fundamental model in information security, representing the three core principles that guide efforts to protect data and systems. Each letter in "CIA" stands for a distinct principle:

### Availability
Ensures that information and systems are accessible to authorized users when needed. 

Techniques: 
* Redundant Systems: Uses multiple backup systems to ensure that resources are available even if one system fails (e.g., multiple servers, data centers).
* Load Balancing: Distributes workloads across multiple systems to prevent overloading and maintain smooth performance.
* Backup and Recovery: Creates and maintains copies of data so it can be restored if lost (e.g., periodic data backups, disaster recovery plans).
* DDoS Protection: Mitigates Distributed Denial of Service attacks that aim to make services unavailable by overwhelming them with requests.
* Regular Maintenance and Patching: Ensures systems are up-to-date and secure, reducing the risk of downtime due to vulnerabilities.

### Confidentiality
Sensitive information is kept private and only accessible to authorized individuals or systems. Encryption is a common technique used to achieve confidentiality by ensuring data in a way that makes it unreadable to unauthorized parties.

Technique:
* Encryption: Converts data into a coded format (e.g., AES, RSA) that can only be read by authorized parties.
* Access Controls: Implements restrictions to ensure only authorized users can access specific data (e.g., role-based access control or attribute-based access control).
* Authentication: Verifies the identity of users (e.g., passwords, multi-factor authentication, biometric verification).
* Data Masking: Obscures sensitive information to limit its visibility (e.g., showing only the last four digits of a credit card number).
* Steganography: Hides data within other files (like images) to avoid detection.

### Integrity
Protects data from unauthorized modifications or tampering, ensuring its accuracy and reliability. Mechanisms like hashing, digital signatures, and checksums are used to verify that information remains consistent and unaltered from its original form.

Technique: 
* Hashing: Generates a unique hash for data (e.g., SHA-256) so that any change in the data can be detected.
* Digital Signatures: Provides a way to verify the authenticity and integrity of messages or documents, often used in combination with public-key encryption.
* Checksums: Creates a small block of data based on file contents to detect accidental or intentional modifications.
* Message Authentication Codes (MACs): Uses cryptographic hashing and a secret key to verify data integrity and authenticity.
* Version Control: Tracks changes to files over time to prevent accidental data loss or unauthorized alterations (e.g., Git for codebases).

# Consistency models
https://jepsen.io/consistency/models#consistency-models

| Consistency Model                     | Description                                                                                       | Pros                                        | Cons                                      |
|---------------------------------------|---------------------------------------------------------------------------------------------------|---------------------------------------------|-------------------------------------------|
| **Linearizability (Single-Copy Atomicity)** | Operations appear instantaneous with real-time ordering.                               | Clear, consistent state                     | High latency in distributed systems       |
| **Strong Consistency**                | Guarantees all clients see the latest write immediately.                                          | High accuracy, avoids conflicts             | High latency due to synchronization       |
| **Sequential Consistency**            | All clients see operations in the same sequential order, though not necessarily in real-time.     | Simpler, often faster than strong consistency| Some synchronization still required       |
| **Causal Consistency**                | Maintains order of causally related operations; unrelated operations may be unordered.            | Good balance of consistency and availability| Complex to implement                      |
| **Release Consistency**               | Updates propagate on acquire/release synchronization points rather than immediately.              | Efficient with controlled synchronization   | More relaxed consistency outside critical sections |
| **Read-Your-Writes Consistency**      | Ensures a client’s reads reflect its own previous writes.                                         | Immediate feedback for interactive apps     | No guarantees for other clients           |
| **Monotonic Read Consistency**        | Ensures clients do not read older versions after seeing newer ones.                               | Logical read progression                    | Requires version tracking                 |
| **Eventual Consistency**              | Ensures all replicas converge to the same state eventually, but reads may be stale initially.     | High availability, low latency              | Temporary inconsistency                   |


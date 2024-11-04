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


> Response Time = Latency + Processing Time

**Response Time**: The time difference between the client sending the request and
receiving the response.

**Latency**: The time the request has to wait before it is processed.

**Processing Time**: The time it takes to process the request

**Throughput**: The number of requests processed per second by
the application

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

## (CIA) triad

The CIA triad represents three core principles in information security, and each of these principles plays a distinct yet interconnected role in safeguarding data and information systems.

### Authenticity
It is essential for verifying the identity of users, systems, or entities interacting with information systems. It prevents unauthorized access by ensuring that only legitimate users gain entry.

Technique: authentication mechanism include something you know (e.g., passwords), something you have (e.g., security tokens), or something you are (e.g., bio-metrics).

### Confidentiality
Sensitive information is kept private and only accessible to authorized individuals or systems. Encryption is a common technique used to achieve confidentiality by ensuring data in a way that makes it unreadable to unauthorized parties.

Technique: Encryption is a common method to achieve confidentiality. By encrypting data, it becomes unreadable to anyone without the proper decryption key.

### Integrity
It focuses on maintaining the accuracy and consistency of data, preventing unauthorized modifications, and ensuring that data remains trustworthy. Hash functions and digital signatures are commonly used to verify the integrity of data.

Technique: hash functions play a significant role in maintaining integrity. When data is hashed, any change to the data results in a different hash value.
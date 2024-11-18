We discussed the three fundamental scalability patterns: functional decomposition, data partitioning, and replication.
They all have one thing in common: they increase the number of
moving parts (machines, services, processes, etc.) in our applications. But since every part has a probability of failing, the more
moving parts there are, the higher the chance that any of them
will fail. Eventually, anything that can go wrong will go wrong;
power outages, hardware faults, software crashes, memory leaks
— you name it.

# Common failure causes
We say that a system has a **failure** when it no longer provides a
service to its users that meets its specification. A failure is caused
by a **fault**: a failure of an internal component or an external dependency the system depends on. Some faults can be tolerated and
have no user-visible impact at all, while others lead to failures.

To build fault-tolerant applications, we first need to have an idea
of what can go wrong.

## Hardware faults
Any physical part of a machine can fail. HDDs, memory modules,
power supplies, motherboards, SSDs, NICs, or CPUs, can all stop
working for various reasons. In some cases, hardware faults can
cause data corruption as well. If that wasn’t enough, entire data
centers can go down because of power cuts or natural disasters.

We can address many of these infrastructure faults with redundancy. You would think that these faults are
the main cause for distributed applications failing, but in reality,
they often fail for very mundane reasons.

## Incorrect error handling
A study from 2014 of user-reported failures from five popular distributed data stores found that the majority of catastrophic failures
were the result of incorrect handling of non-fatal errors.

In most cases, the bugs in the error handling could have been detected with simple tests. For example, some handlers completely
ignored errors. Others caught an overly generic exception, like Exception in Java, and aborted the entire process for no good reason.
And some other handlers were only partially implemented and
even contained “FIXME” and “TODO” comments.

## Configuration changes
Configuration changes are one of the leading root causes for catastrophic failures. It’s not just misconfigurations that cause problems, but also valid configuration changes to enable rarely-used
features that no longer work as expected (or never did).

What makes configuration changes particularly dangerous is that
their effects can be delayed. If an application reads a configuration value only when it’s actually needed, an invalid value might
take effect only hours or days after it has changed and thus escape
early detection.

This is why configuration changes should be version-controlled,
tested, and released just like code changes, and their validation
should happen preventively when the change happens.

## Single points of failure
A single point of failure (SPOF) is a component whose failure
brings the entire system down with it. In practice, systems can
have multiple SPOFs.

Humans make for great SPOFs, and if you put them in a position where they can cause a catastrophic failure on their own, you
can bet they eventually will. For example, human failures often
happen when someone needs to manually execute a series of operational steps in a specific order without making any mistakes.
On the other hand, computers are great at executing instructions,
which is why automation should be leveraged whenever possible.

Another common SPOF is DNS6. If clients can’t resolve the domain name for an application, they won’t be able to connect to
it. There are many reasons why that can happen, ranging from domain names expiring to entire root level domains going down.

Similarly, the TLS certificate used by an application for its HTTP
endpoints is also a SPOF. If the certificate expires, clients won’t
be able to open a secure connection with the application.

Ideally, SPOFs should be identified when the system is designed.
The best way to detect them is to examine every system component
and ask what would happen if it were to fail. Some SPOFs can be
architected away, e.g., by introducing redundancy, while others
can’t. In that case, the only option left is to reduce the SPOF’s blast
radius, i.e., the damage the SPOF inflicts on the system when it
fails. Many of the resiliency patterns we will discuss later reduce
the blast radius of failures.

## Network faults
When a client sends a request to a server, it expects to receive a
response from it a while later. In the best case, it receives the response shortly after sending the request. If that doesn’t happen,
the client has two options: continue to wait or fail the request with
a time-out exception or error.

When the concepts of failure detection
and timeouts were introduced, there are many reasons for not getting a prompt response. For example, the server could be very
slow or have crashed while processing the request; or maybe the
network could be losing a small percentage of packets, causing lots
of retransmissions and delays.

Slow network calls are the silent killers of distributed systems.
Because the client doesn’t know whether the response will eventually arrive, it can spend a long time waiting before giving up, if
it gives up at all, causing performance degradations that are challenging to debug. This kind of fault is also referred to as a gray
failure: a failure that is so subtle that it can’t be detected quickly
or accurately. Because of their nature, gray failures can easily bring
an entire system down to its knees.

## Resource leaks
From an observer’s point of view, a very slow process is not very
different from one that isn’t running at all — neither can perform
useful work. Resource leaks are one of the most common causes
of slow processes.

Memory is arguably the most well-known resource affected by
leaks. A memory leak causes a steady increase in memory consumption over time. Even languages with garbage collection are
vulnerable to leaks: if a reference to an object that is no longer
needed is kept somewhere, the garbage collector won’t be able to
delete it. When a leak has consumed so much memory that there
is very little left, the operating system will start to swap memory
pages to disk aggressively. Also, the garbage collector will kick in
more frequently, trying to release memory. All of this consumes
CPU cycles and makes the process slower. Eventually, when there
is no more physical memory left, and there is no more space in the
swap file, the process won’t be able to allocate memory, and most
operations will fail.

Memory is just one of the many resources that can leak. Take
thread pools, for example: if a thread acquired from a pool makes
a synchronous blocking HTTP call without a timeout and the call
never returns, the thread won’t be returned to the pool. And since
the pool has a limited maximum size, it will eventually run out of
threads if it keeps losing them.

You might think that making asynchronous calls rather than synchronous ones would help in the previous case. However, modern
HTTP clients use socket pools to avoid recreating TCP connections
and paying a performance fee. If a request is made without a timeout, the connection is never returned
to the pool. As the pool has a limited maximum size, eventually,
there won’t be any connections left.

On top of that, your code isn’t the only thing accessing memory,
threads, and sockets. The libraries your application depends on
use the same resources, and they can hit the same issues we just discussed.

## Load pressure
Every system has a limit of how much load it can withstand, i.e.,
its capacity. So when the load directed to the system continues
to increase, it’s bound to hit that limit sooner or later. But an organic increase in load, that gives the system the time to scale out
accordingly and increase its capacity, is one thing, and a sudden
and unexpected flood is another.

For example, consider the number of requests received by an application in a period of time. The rate and the type of incoming
requests can change over time, and sometimes suddenly, for a variety of reasons:
* The requests might have a seasonality. So, for example, depending on the hour of the day, the application is hit by users
in different countries.
* Some requests are much more expensive than others and
abuse the system in unexpected ways, like scrapers slurping
in data at super-human speed.
* Some requests are malicious, like those of DDoS attacks that
try to saturate the application’s bandwidth to deny legitimate users access to it.

While some load surges can be handled by automation that adds
capacity (e.g., autoscaling), others require the system to reject requests to shield it from overloading.

## Cascading failures
You would think that if a system has hundreds of processes, it
shouldn’t make much of a difference if a small percentage are slow
or unreachable. The thing about faults is that they have the potential to spread virally and cascade from one process to the other
until the whole system crumbles to its knees. This happens when system components depend on each other, and a failure in one increases the probability of failure in others.

## Managing risk
As it should be evident by now, a distributed application needs to
accept that faults are inevitable and be prepared to detect, react to,
and repair them as they occur.

We first have to consider the probability it will manifest
and the impact it will cause to the system’s users when it does. By
multiplying the two factors together, we get a risk score that we
can use to prioritize which faults to address first.
For example, a fault that is very likely to happen, and has a large
impact, should be tackled head on; on the other hand, a fault with
a low likelihood and low impact can wait.

Once we decide that we need to do something about a specific fault,
we can try to reduce its probability and/or reduce its impact.

# Redundancy
Redundancy, the replication of functionality or state, is arguably
the first line of defense against failures. When functionality or state
is replicated over multiple nodes and a node fails, the others can
take over. Moreover, as discussed before, replication is also a
core pattern that enables our applications to scale out horizontally.

Redundancy is the main reason why distributed applications can
achieve better availability than single-node applications. But only
some forms of redundancy actually improve availability. Marc
Brooker lists four prerequisites:
1. The complexity added by introducing redundancy mustn’t
cost more availability than it adds.
2. The system must reliably detect which of the redundant com-
ponents are healthy and which are unhealthy.
3. The system must be able to run in degraded mode.
4. The system must be able to return to fully redundant mode.

Let’s see how these prerequisites apply to a concrete example.
Hardware faults such as disk, memory, and network failures can
cause a node to crash, degrade or become otherwise unavailable.
In a stateless service, a load balancer can mask these faults using a pool of redundant nodes. Although the load balancer increases
the system’s complexity and, therefore, the number of ways the
system can fail, the benefits in terms of scalability and availability
almost always outweigh the risks it introduces (e.g., the load
balancer failing).

The load balancer needs to detect which nodes are healthy and
which aren’t to take the faulty ones out of the pool. It does that
with health checks. Health checks
are critical to achieving high availability; if there are ten servers
in the pool and one is unresponsive for some reason, then 10%
of requests will fail, causing the availability to drop. Therefore,
the longer it takes for the load balancer to detect the unresponsive
server, the longer the failures will be visible to the clients.

Now, when the load balancer takes one or more unhealthy servers
out of the pool, the assumption is that the others have enough capacity left to handle the increase in load. In other words, the system must be able to run in degraded mode. However, that by itself
is not enough; new servers also need to be added to the pool to
replace the ones that have been removed. Otherwise, there eventually won’t be enough servers left to cope with the load.

In stateful services, masking a node failure is a lot more complex
since it involves replicating state. We have discussed replication at
length in the previous chapters, and it shouldn’t come as a surprise
by now that meeting the above requisites is a lot more challenging
for a stateful service than for a stateless one.

## Correlation
Redundancy is only helpful when the redundant nodes can’t fail
for the same reason at the same time, i.e., when failures are not correlated. For example, if a faulty memory module causes a server
to crash, it’s unlikely other servers will fail simultaneously for the
same reason since they are running on different machines. However, if the servers are hosted in the same data center, and a fiber
cut or an electrical storm causes a data-center-wide outage, the entire application becomes unavailable no matter how many servers
there are. In other words, the failures caused by a data center outage are correlated and limit the application’s availability. So if we
want to increase the availability, we have to reduce the correlation
between failures by using more than one data center.

Cloud providers such as AWS and Azure replicate their entire
stack in multiple regions for that very reason. Each region
comprises multiple data centers called Availability Zones (AZs)
that are cross-connected with high-speed network links. AZs are
far enough from each other to minimize the risk of correlated
failures (e.g., power cuts) but still close enough to have low
network latency, which is bounded by the speed of light. In fact,
the latency is low enough by design to support synchronous
replication protocols without a significant latency penalty.

With AZs, we can create applications that are resilient to data center outages. For example, a stateless service could have instances
running in multiple AZs behind a shared load balancer so that if
an AZ becomes unavailable, it doesn’t impact the availability of
the service. On the other hand, stateful services require the use
of a replication protocol to keep their state in sync across AZs.
But since latencies are low enough between AZs, the replication
protocol can be partially synchronous, like Raft, or even fully synchronous, like chain replication.

Taking it to the extreme, a catastrophic event could destroy an en-
tire region with all of its AZs. To tolerate that, we can duplicate
the entire application stack in multiple regions. To distribute the
traffic to different data centers located in different regions, we can
use *global DNS load balancing*. Unlike earlier, the application’s state
needs to be replicated asynchronously across regions given the
high network latency between regions.

That said, the chance of an entire region being destroyed is extremely low. Before embarking on the effort of making your application resilient against region failures, you should have very good reasons for it. It’s more likely your application will be forced to
have a presence in multiple regions for legal compliance reasons.
For example, there are laws mandating that the data of European
customers has to be processed and stored within Europe.

# Fault isolation
So far, we have discussed how to address infrastructure faults with
redundancy, but there are other kinds of failures that we can’t tolerate with redundancy alone because of their high degree of corre-
lation.

For example, suppose a specific user sends malformed requests
(deliberately or not) that cause the servers handling them to crash
because of a bug. Since the bug is in the code, it doesn’t matter how
many DCs and regions our application is deployed to; if the user’s
requests can land anywhere, they can affect all DCs and regions.
Due to their nature, these requests are sometimes referred to as
**poison pills**.

Similarly, if the requests of a specific user require a lot more resources than others, they can degrade the performance for every
other user (aka **noisy neighbor effect**).

The main issue in the previous examples is that the blast radius
of poison pills and noisy neighbors is the entire application. To
reduce it, we can partition the application’s stack by user so that
the requests of a specific user can only ever affect the partition it
was assigned to. That way, even if a user is degrading a partition, the issue is isolated from the rest of the system.

For example, suppose we have 6 instances of a stateless service
behind a load balancer, divided into 3 partitions.
In this case, a noisy or poisonous user can only ever impact 33
percent of users. And as the number of partitions increases, the
blast radius decreases further.

The use of partitions for fault isolation is also referred to as the
**bulkhead pattern**, named after the compartments of a ship’s hull. If
one compartment is damaged and fills up with water, the leak is
isolated to that partition and doesn’t spread to the rest of the ship.

## Shuffle sharding
The problem with partitioning is that users who are unlucky
enough to land on a degraded partition are impacted as well. For
stateless services, there is a very simple, yet powerful, variation of
partitioning called **shuffle sharding** that can help mitigate that.

The idea is to introduce **virtual partitions** composed of random (but permanent) subsets of service instances. This makes it much more
unlikely for two users to be allocated to the same partition as each
other.

By combining shuffle
sharding with a load balancer that removes faulty instances, and
clients that retry failed requests, we can build a system with much
better fault isolation than one with physical partitions alone.

## Cellular architecture
In the previous examples, we discussed partitioning in the context
of stateless services. We can take it up a notch and partition the entire application stack, including its dependencies (load balancers,
compute services, storage services, etc.), by user into **cells**. Each
cell is completely independent of others, and a gateway service is
responsible for routing requests to the right cells.

We have already seen an example of a “cellular” architecture when
discussing Azure Storage. In Azure Storage, a cell is
a storage cluster, and accounts are partitioned across storage clusters.

An unexpected benefit of cellular architectures comes from setting
limits to the maximum capacity of a cell. That way, when the system needs to scale out, a new cell is added rather than scaling out
existing ones. Since a cell has a maximum size, we can thoroughly
test and benchmark it at that size, knowing that we won’t have any
surprises in the future and hit some unexpected brick wall.


# System models

To reason about distributed systems, we need to define precisely
what can and can’t happen. A *system model* encodes expectations
about the behavior of processes, communication links, and timing;
think of it as a set of assumptions that allow us to reason about
distributed systems by ignoring the complexity of the actual technologies used to implement them.

For example, these are some common models for communication
links:
* The *fair-loss* link model assumes that messages may be lost
and duplicated, but if the sender keeps retransmitting a message, eventually it will be delivered to the destination.
* The *reliable link* model assumes that a message is delivered
exactly once, without loss or duplication (correct, complete, and ordered delivery). A reliable link can
be implemented on top of a fair-loss one by de-duplicating
messages at the receiving side. 
* The authenticated reliable link model makes the same assumptions as the reliable link but additionally assumes that the
receiver can authenticate the sender.

Similarly, we can model the behavior of processes based on the
type of failures we expect to happen:
* The *arbitrary-fault* model assumes that a process can deviate
from its algorithm in arbitrary ways, leading to crashes or
unexpected behaviors caused by bugs or malicious activity.
For historical reasons, this model is also referred to as the
“Byzantine” model. More interestingly, it can be theoretically
proven that a system using this model can tolerate up to 1/3 of
faulty processes and still operate correctly.
* The *crash-recovery* model assumes that a process doesn’t deviate from its algorithm but can crash and restart at any time,
losing its in-memory state.
* The *crash-stop* model assumes that a process doesn’t deviate
from its algorithm but doesn’t come back online if it crashes.
Although this seems unrealistic for software crashes, it models unrecoverable hardware faults and generally makes the
algorithms simpler.

The arbitrary-fault model is typically used to model safety-critical
systems like airplane engines, nuclear power plants, and systems
where a single entity doesn’t fully control all the processes (e.g.,
digital cryptocurrencies such as Bitcoin). These use cases are outside the scope, and the algorithms presented here will generally assume a **crash-recovery** model.

Finally, we can also model timing assumptions:
* The *synchronous* model assumes that sending a message
or executing an operation never takes more than a certain
amount of time. This is not very realistic for the type
of systems we care about, where we know that sending
messages over the network can potentially take a very long time, and processes can be slowed down by, e.g., garbage
collection cycles or page faults.
* The *asynchronous* model assumes that sending a message or
executing an operation on a process can take an unbounded
amount of time. Unfortunately, many problems can’t be
solved under this assumption; if sending messages can take
an infinite amount of time, algorithms can get stuck and
not make any progress at all. Nevertheless, this model is
useful because it’s simpler than models that make timing
assumptions, and therefore algorithms based on it are also
easier to implement.
* The *partially synchronous* model assumes that the system behaves synchronously most of the time. This model is typically representative enough of real-world systems.

# Failure detection
Several things can go wrong when a client sends a request to a
server. In the best case, the client sends a request and receives a
response. But what if no response comes back after some time?
In that case, it’s impossible to tell whether the server is just very
slow, it crashed, or a message couldn’t be delivered because of a
network issue.

The client can configure a timeout to trigger if it hasn’t received
a response from the server after a certain amount of time. If and
when the timeout triggers, the client considers the server unavailable and either throws an error or retries the request.

The tricky part is deciding how long to wait for the timeout to trigger. If the delay is too short, the client might wrongly assume the
server is unavailable; if the delay is too long, the client might waste
time waiting for a response that will never arrive. In summary, it’s
not possible to build a perfect failure detector.

But a process doesn’t need to wait to send a message to find out
that the destination is not reachable. It can also proactively try to
maintain a list of available processes using pings or heartbeats.

A *ping* is a periodic request that a process sends to another to check
whether it’s still available. The process expects a response to the
ping within a specific time frame. If no response is received, a timeout triggers and the destination is considered unavailable. How-
ever, the process will continue to send pings to it to detect if and
when it comes back online.

A *heartbeat* is a message that a process periodically sends to another.
If the destination doesn’t receive a heartbeat within a specific time
frame, it triggers a timeout and considers the process unavailable.
But if the process comes back to life later and starts sending out
heartbeats, it will eventually be considered to be available again.

Pings and heartbeats are generally used for processes that interact
with each other frequently, in situations where an action needs to
be taken as soon as one of them is no longer reachable. In other circumstances, detecting failures just at communication time is good
enough.

Key Differences
* Scope: Ping checks only basic connectivity at the network layer, while heartbeat checks the actual health and operational status of a component at the application level.
* Frequency and Automation: Heartbeats are typically automated and continuous, making them ideal for live monitoring. Ping is often used manually or at less frequent intervals.

# Time

Time is an essential concept in any software application; even more
so in distributed ones. We have seen it play a crucial role in the network stack (e.g., DNS record TTL) and failure detection (timeouts).
Another important use of it is for ordering events.

The flow of execution of a single-threaded application is simple to
understand because every operation executes sequentially in time,
one after the other. But in a distributed system, there is no shared
global clock that all processes agree on that can be used to order
operations. And, to make matters worse, processes can run concurrently.

## Physical clocks
A process has access to a physical wall-time clock. The most common type is based on a vibrating quartz crystal, which is cheap but
not very accurate. Depending on manufacturing differences and external temperature, one quartz clock can run slightly faster or
slower than others. The rate at which a clock runs faster or slower
is also called *clock drift*. In contrast, the difference between two
clocks at a specific point in time is referred to as *clock skew*.

Because quartz clocks drift, they need to be synced periodically
with machines that have access to higher-accuracy clocks, like
atomic ones. Atomic clocks measure time based on quantum-mechanical properties of atoms. They are significantly more
expensive than quartz clocks and accurate to 1 second in 3 million
years.

The synchronization between clocks can be implemented with a
protocol, and the challenge is to do so despite the unpredictable
latencies introduced by the network. The most commonly used
protocol is the *Network Time Protocol* (NTP). In NTP, a client estimates the clock skew by receiving a timestamp from a NTP server
and correcting it with the estimated network latency. With an estimate of the clock skew, the client can adjust its clock. However,
this causes the clock to jump forward or backward in time, which
creates a problem when comparing timestamps. For example, an
operation that runs after another could have an earlier timestamp
because the clock jumped back in time between the two operations.

Luckily, most operating systems offer a different type of clock that
is not affected by time jumps: a *monotonic clock*. A monotonic clock
measures the number of seconds elapsed since an arbitrary point
in time (e.g., boot time) and can only move forward. A monotonic
clock is useful for measuring how much time has elapsed between
two timestamps on the same node. However, monotonic clocks
are of no use for comparing timestamps of different nodes.

Since we don’t have a way to synchronize wall-time clocks across
processes perfectly, we can’t depend on them for ordering operations across nodes. To solve this problem, we need to look at it
from another angle. We know that two operations can’t run concurrently in a single-threaded process as one must happen before
the other. This *happened-before* relationship creates a *causal* bond
between the two operations, since the one that happens first can
have side-effects that affect the operation that comes after it. We
can use this intuition to build a different type of clock that isn’t
tied to the physical concept of time but rather captures the causal
relationship between operations: a logical clock.

## Logical clocks
A *logical clock* measures the passing of time in terms of logical operations, not wall-clock time. The simplest possible logical clock is
a counter, incremented before an operation is executed. Doing so
ensures that each operation has a distinct *logical timestamp*. If two
operations execute on the same process, then necessarily one must
come before the other, and their logical timestamps will reflect that.
But what about operations executed on different processes?

Imagine sending an email to a friend. Any actions you did before
sending that email, like drinking coffee, must have happened before the actions your friend took after receiving the email. Similarly, when one process sends a message to another, a so-called
*synchronization point* is created. The operations executed by the
sender before the message was sent *must* have happened before
the operations that the receiver executed after receiving it.

A *Lamport clock* is a logical clock based on this idea. To implement
it, each process in the system needs to have a local counter that
follows specific rules:
* The counter is initialized with 0.
* The process increments its counter by 1 before executing an
operation.
* When the process sends a message, it increments its counter
by 1 and sends a copy of it in the message.
* When the process receives a message, it merges the counter it received with its local counter by taking the maximum of
the two. Finally, it increments the counter by 1.


However, two unrelated operations can have the same logical
timestamp. To create a strict total order, we can
arbitrarily order the processes to break ties. Regardless of whether ties are broken, the order of logical timestamps doesn’t imply a causal relationship. To guarantee this relationship, we have to use a different type of logical clock: a *vector clock*.

## Vector clocks
A vector clock is a logical clock that guarantees that if a logical
timestamp is less than another, then the former must have
happened-before the latter. A vector clock is implemented with
an array of counters, one for each process in the system. And, as
with Lamport clocks, each process has its local copy.

For example, suppose the system is composed of three processes,
𝑃 1, 𝑃 2, and 𝑃 3. In this case, each process has a local vector clock
implemented with an array of three counters [𝐶𝑃 1, 𝐶𝑃 2, 𝐶𝑃 3].
The first counter in the array is associated with 𝑃 1, the second
with 𝑃 2, and the third with 𝑃 3.

A process updates its local vector clock based on the following
rules:
* Initially, the counters in the array are set to 0.
* When an operation occurs, the process increments its counter
in the array by 1.
* When the process sends a message, it increments its counter
in the array by 1 and sends a copy of the array with the mes-
sage.
* When the process receives a message, it merges the array it
received with the local one by taking the maximum of the
two arrays element-wise. Finally, it increments its counter in
the array by 1.

The beauty of vector clock timestamps is that they can be partially
ordered; given two operations 𝑂1 and 𝑂2 with timestamps 𝑇1
and 𝑇2, if:
* every counter in 𝑇1 is less than or equal to the corresponding
counter in 𝑇2,
* and there is at least one counter in 𝑇1 that is strictly less than
the corresponding counter in 𝑇2,
then 𝑂1 happened-before 𝑂2. 

If 𝑂1 didn’t happen-before 𝑂2 and 𝑂2 didn’t happen-before 𝑂1,
then the timestamps can’t be ordered, and the operations are considered to be concurrent.

One problem with vector clocks is that the storage requirement on
each process grows linearly with the number of processes, which
becomes a problem for applications with many clients. However,
there are other types of logical clocks that solve this issue, like dotted version vectors.

# Leader election

There are times when a single process in the system needs to have
special powers, like accessing a shared resource or assigning work
to others. To grant a process these powers, the system needs to
elect a leader among a set of candidate processes, which remains in
charge until it relinquishes its role or becomes otherwise unavailable. When that happens, the remaining processes can elect a new
leader among themselves.

A leader election algorithm needs to guarantee that there is at most
one leader at any given time and that an election eventually completes even in the presence of failures. These two properties are
also referred to as *safety* and *liveness*, respectively, and they are general properties of distributed algorithms. Informally, safety guarantees that nothing bad happens and liveness that something good
eventually does happen. In this chapter, we will explore how a
specific algorithm, the Raft leader election algorithm, guarantees
these properties.

## Raft leader election
Raft’s leader election algorithm is implemented as a state machine
in which any process is in one of three states:
* the *follower state*, where the process recognizes another one
as the leader;
* the *candidate state*, where the process starts a new election
proposing itself as a leader;
* or the *leader state*, where the process is the leader.

In Raft, time is divided into election terms of arbitrary length that
are numbered with consecutive integers (i.e., logical timestamps).
A term begins with a new election, during which one or more candidates attempt to become the leader. The algorithm guarantees
that there is at most one leader for any term. But what triggers an
election in the first place?

When the system starts up, all processes begin their journey as followers. A follower expects to receive a periodic heartbeat from
the leader containing the election term the leader was elected in.
If the follower doesn’t receive a heartbeat within a certain period
of time, a timeout fires and the leader is presumed dead. At that
point, the follower starts a new election by incrementing the current term and transitioning to the candidate state. It then votes for
itself and sends a request to all the processes in the system to vote
for it, stamping the request with the current election term.

The process remains in the candidate state until one of three things
happens: it wins the election, another process wins the election, or
some time goes by with no winner:
some time goes by with no winner:
* **The candidate wins the election** — The candidate wins the
election if the majority of processes in the system vote for
it. Each process can vote for at most one candidate in a term
on a first-come-first-served basis. This majority rule enforces
that at most one candidate can win a term. If the candidate
wins the election, it transitions to the leader state and starts sending heartbeats to the other processes.
* **Another process wins the election** — If the candidate receives a heartbeat from a process that claims to be the leader
with a term greater than or equal to the candidate’s term, it
accepts the new leader and returns to the follower state. If
not, it continues in the candidate state. You might be wondering how that could happen; for example, if the candidate
process was to stop for any reason, like for a long garbage collection pause, by the time it resumes another process could
have won the election.
* **A period of time goes by with no winner** — It’s unlikely but
possible that multiple followers become candidates simultaneously, and none manages to receive a majority of votes;
this is referred to as a split vote. The candidate will eventually time out and start a new election when that happens.
The election timeout is picked randomly from a fixed interval to reduce the likelihood of another split vote in the next
election.

## Practical considerations
There are other leader election algorithms out there, but Raft’s
implementation is simple to understand and also widely used
in practice. In practice,
you will rarely, if ever, need to implement leader election from
scratch. A good reason for doing that would be if you needed
a solution with zero external dependencies. Instead, you can
use any *fault-tolerant* key-value store that offers a linearizable
*compare-and-swap* operation with an expiration time (TTL).

The compare-and-swap operation atomically updates the value of
a key if and only if the process attempting to update the value correctly identifies the current value. The operation takes three parameters: 𝐾, 𝑉𝑜, and 𝑉𝑛, where 𝐾 is a key, and 𝑉𝑜 and 𝑉𝑛 are
values referred to as the old and new value, respectively. The operation atomically compares the current value of 𝐾 with 𝑉𝑜, and
if they match, it updates the value of 𝐾 to 𝑉𝑛. If the values don’t
match, then 𝐾 is not modified, and the operation fails.

The expiration time defines the time to live for a key, after which
the key expires and is removed from the store unless the expiration
time is extended. The idea is that each competing process tries
to acquire a *lease* by creating a new key with compare-and-swap.
The first process to succeed becomes the leader and remains such
until it stops renewing the lease, after which another process can
become the leader.

The expiration logic can also be implemented on the client side, like the locking library for DynamoDB does, but the implementation is more complex, and it still requires the data store to offer
a compare-and-swap operation.

You might think that’s enough to guarantee there can’t be more
than one leader at any given time. But, unfortunately, that’s not
the case. To see why suppose multiple processes need to update a
file on a shared file store, and we want to guarantee that only one at
a time can access it to avoid race conditions. Now, suppose we use
a lease to lock the critical section. Each process tries to acquire the
lease, and the one that does so successfully reads the file, updates
it in memory, and writes it back to the store. 

The issue is that by the time the process gets to write to the file, it
might no longer hold the lease. For example, the operating system
might have preempted and stopped the process for long enough
for the lease to expire. The process could try to detect that by comparing the lease expiration time to its local clock before writing to
the store, assuming clocks are synchronized. 

However, clock synchronization isn’t perfectly accurate. On top of
that, the lease could expire while the request to the store is in-flight
because of a network delay. To account for these problems, the
process could check that the lease expiration is far enough in the
future before writing to the file. Unfortunately, this workaround
isn’t foolproof, and the lease can’t guarantee mutual exclusion by
itself.

To solve this problem, we can assign a version number to each file that is incremented every time the file is updated. The process
holding the lease can then read the file and its version number from
the file store, do some local computation, and finally update the
file (and increment the version number) conditional on the version
number not having changed. The process can perform this validation atomically using a compare-and-swap operation, which many
file stores support.

If the file store doesn’t support conditional writes, we have to design around the fact that occasionally there will be a race condition.
Sometimes, that’s acceptable; for example, if there are momentarily two leaders and they both perform the same idempotent update, no harm is done.

Although having a leader can simplify the design of a system as it
eliminates concurrency, it can also become a scalability bottleneck
if the number of operations performed by it increases to the point
where it can no longer keep up. Also, a leader is a single point of
failure with a large blast radius; if the election process stops working or the leader isn’t working as expected, it can bring down the
entire system with it. We can mitigate some of these downsides
by introducing partitions and assigning a different leader per partition, but that comes with additional complexity. This is the solution many distributed data stores use since they need to use partitioning anyway to store data that doesn’t fit in a single node.

As a rule of thumb, if we must have a leader, we have to minimize
the work it performs and be prepared to occasionally have more
than one.

Taking a step back, a crucial assumption we made earlier is that
the data store that holds leases is fault-tolerant, i.e., it can tolerate
the loss of a node. Otherwise, if the data store ran on a single node
and that node were to fail, we wouldn’t be able to acquire leases.
For the data store to withstand a node failing, it needs to replicate
its state over multiple nodes.
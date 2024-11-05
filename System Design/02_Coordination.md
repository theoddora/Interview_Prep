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

## Replication
Data replication is a fundamental building block of distributed systems. One reason for replicating data is to increase availability. If
some data is stored exclusively on a single process, and that process goes down, the data won’t be accessible anymore. However,
if the data is replicated, clients can seamlessly switch to a copy.
Another reason for replication is to increase scalability and performance; the more replicas there are, the more clients can access the
data concurrently.

Implementing replication is challenging because it requires keeping replicas consistent with one another even in the face of failures. In this chapter, we will explore Raft’s replication algorithm,
a replication protocol that provides the strongest consistency guarantee possible — the guarantee that to the clients, the data appears
to be stored on a single process, even if it’s actually replicated.
Arguably, the most popular protocol that offers this guarantee is
Paxos, but we will discuss Raft as it’s more understandable.

Raft is based on a mechanism known as *state machine replication*.
The main idea is that a single process, the leader, *broadcasts* operations that change its state to other processes, the followers (or
replicas). If the followers execute the same sequence of operations
as the leader, then each follower will end up in the same state as
the leader. Unfortunately, the leader can’t simply broadcast operations to the followers and call it a day, as any process can fail at
any time, and the network can lose messages. This is why a large
part of the algorithm is dedicated to fault tolerance.

The reason why this this mechanism is called stated machine replication is that each process is modeled as a *state machine* that transitions from one state to another in response to some input (an operation). If the state machines are *deterministic* and get exactly the
same input in the same order, their states are consistent. That way,
if one of them fails, a redundant copy is available from any of the
other state machines. State machine replication is a very powerful
tool to make a service fault-tolerant as long it can be modeled as a
state machine.

## State machine replication

When the system starts up, a leader is elected using Raft’s leader
election algorithm which doesn’t require any external dependencies. The leader is the only process that can
change the replicated state. It does so by storing the sequence of
operations that alter the state into a local *log*, which it replicates
to the followers. Replicating the log is what allows the state to be
kept in sync across processes.

A log is an ordered list of entries where
each entry includes:
* the operation to be applied to the state. The operation needs to be deterministic so that all followers end up in the same state, but it can be arbitrarily complex as long as that requirement is respected (e.g., compare-
and-swap or a transaction with multiple operations);
* the index of the entry’s position in the log;
* and the leader’s election term (the number in each box).

When the leader wants to apply an operation to its local state, it first appends a new entry for the operation to its log. At this point,
the operation hasn’t been applied to the local state just yet; it has
only been logged.

The leader then sends an *AppendEntries* request to each follower
with the new entry to be added. This message is also sent out periodically, even in the absence of new entries, as it acts as a *heartbeat*
for the leader.

When a follower receives an *AppendEntries* request, it appends the
entry it received to its own log (without actually executing the operation yet) and sends back a response to the leader to acknowledge that the request was successful. When the leader hears back
successfully from a majority of followers, it considers the entry to
be committed and executes the operation on its local state. The
leader keeps track of the highest committed index in the log, which
is sent in all future *AppendEntries* requests. A follower only applies
a log entry to its local state when it finds out that the leader has
committed the entry.

Because the leader needs to wait for *only* a majority (quorum) of
followers, it can make progress even if some are down, i.e., if there
are 2𝑓 + 1 followers, the system can tolerate up to 𝑓 failures. The
algorithm guarantees that an entry that is committed is durable
and will eventually be executed by all the processes in the system,
not just those that were part of the original majority.

So far, we have assumed there are no failures, and the network
is reliable. Let’s relax those assumptions. If the leader fails, a
follower is elected as the new leader. But, there is a caveat: because the replication algorithm only needs a majority of processes
to make progress, it’s possible that some processes are not up to
date when a leader fails. To avoid an out-of-date process becoming the leader, a process can’t vote for one with a less up-to-date
log. In other words, a process can’t win an election if it doesn’t
contain all committed entries.

To determine which of two processes’ logs is more up-to-date, the
election term and index of their last entries are compared. If the
logs end with different terms, the log with the higher term is more up to date. If the logs end with the same term, whichever log is
longer is more up to date. Since the election requires a majority
vote, and a candidate’s log must be at least as up to date as any
other process in that majority to win the election, the elected process will contain all committed entries.

If an *AppendEntries* request can’t be delivered to one or more followers, the leader will retry sending it indefinitely until a majority
of the followers have successfully appended it to their logs. Retries are harmless as AppendEntries requests are idempotent, and
followers ignore log entries that have already been appended to
their logs.

If a follower that was temporarily unavailable comes back online,
it will eventually receive an *AppendEntries* message with a log entry from the leader. The *AppendEntries* message includes the index
and term number of the entry in the log that immediately precedes
the one to be appended. If the follower can’t find a log entry with
that index and term number, it rejects the message to prevent creating a gap in its log.

When the *AppendEntries* request is rejected, the leader retries the
request, this time including the last two log entries — this is why
we referred to the request as *AppendEntries* and not as *AppendEntry*.
If that fails, the leader retries sending the last three log entries and
so forth. The goal is for the leader to find the latest log entry where
the two logs agree, delete any entries in the follower’s log after that
point, and append to the follower’s log all of the leader’s entries
after it.

## Consensus
By solving state machine replication, we actually found a solution
to *consensus* — a fundamental problem studied in distributed systems research in which a group of processes has to decide a value so that:
* every non-faulty process eventually agrees on a value;
* the final decision of every non-faulty process is the same everywhere;
* and the value that has been agreed on has been proposed by
a process.

This may sound a little bit abstract. Another way to think about
consensus is as the API of a write-once register (WOR): a thread-
safe and linearizable register that can only be written once but can
be read many times. 

There are plenty of practical applications of consensus. For example, agreeing on which process in a group can acquire a lease requires consensus. And, as mentioned earlier, state machine replication also requires it. If you squint a little, you should be able to
see how the replicated log in Raft is a sequence of WORs, and so
Raft really is just a sequence of consensus instances.

While it’s important to understand what consensus is and how it
can be solved, you will likely never need to implement it from
scratch. Instead, you can use one of the many off-the-shelf solutions available.

For example, one of the most common uses of consensus is for coordination purposes, like the election of a leader. Leader election can be implemented by acquiring a lease. The lease
ensures that at most one process can be the leader at any time and
if the process dies, another one can take its place. However, this
mechanism requires the lease manager, or coordination service, to
be fault-tolerant. Etcd and ZooKeeper are two widely used coordination services that replicate their state for fault-tolerance us-
ing consensus. A coordination service exposes a hierarchical, key-
value store through its API, and also allows clients to watch for
changes to keys. So, for example, acquiring a lease can be implemented by having a client attempt to create a key with a specific
TTL. If the key already exists, the operation fails guaranteeing that
only one client can acquire the lease.

## Consistency models

We discussed state machine replication with the goal of implementing a data store that can withstand failures and scale out to serve
a larger number of requests. Now that we know how to build a
replicated data store in principle, let’s take a closer look at what
happens when a client sends a request to it. In an ideal world, the
request executes instantaneously.

But in reality, things are quite different — the request needs to
reach the leader, which has to process it and send back a response
to the client. These actions take time and
are not instantaneous.

The best guarantee the system can provide is that the request
executes somewhere between its invocation and completion time.
You might think that this doesn’t look like a big deal; after all, it’s what you are used to when writing single-threaded applications. But when you deal
with replicated systems, all bets are off. Let’s see why that’s the
case.

We looked at how Raft replicates the leader’s state
to its followers. Since only the leader can make changes to the state,
any operation that modifies it needs to necessarily go through the
leader. But what about reads? They don’t necessarily have to go
through the leader as they don’t affect the system’s state. Reads
can be served by the leader, a follower, or a combination of leader
and followers. If all reads have to go through the leader, the read
throughput would be limited to that of a single process. But, if any
follower can serve reads instead, then two clients, or observers, can
have a different view of the system’s state since followers can lag
behind the leader.

Intuitively, there is a tradeoff between how consistent the observers’ views of the system are and the system’s performance
and availability. To understand this relationship, we need to
define precisely what we mean by consistency. We will do so with the help of *consistency models*, which formally define the possible
views the observers can have of the system’s state.

### Strong consistency
If clients send writes and reads exclusively to the leader, then every
request appears to take place atomically at a very specific point in
time as if there were a single copy of the data. No matter how many
replicas there are or how far behind they are lagging, as long as the
clients always query the leader directly, there is a single copy of the
data from their point of view.

Because a request is not served instantaneously, and there is a single process that can serve it, the request executes somewhere between its invocation and completion time. By the time it completes, its side-effects are visible to all observers.

Since a request becomes visible to all other participants between
its invocation and completion time, a **real-time guarantee** must
be enforced; this guarantee is formalized by a consistency model
called *linearizability*, or *strong consistency*. Linearizability is the
strongest consistency guarantee a system can provide for single-object requests.

Unfortunately, the leader can’t serve reads directly from its local
state because by the time it receives a request from a client, it might
no longer be the leader; so, if it were to serve the request, the system wouldn’t be strongly consistent. The presumed leader first
needs to contact a majority of replicas to confirm whether it still
is the leader. Only then is it allowed to execute the request and
send back a response to the client. Otherwise, it transitions to the
follower state and fails the request. This confirmation step considerably increases the time required to serve a read.

### Sequential consistency
So far, we have discussed serializing all reads through the leader.
But doing so creates a single chokepoint, limiting the system’s
throughput. On top of that, the leader needs to contact a majority
of followers to handle a read, which increases the time it takes
to process a request. To increase the read performance, we could
also allow the followers to handle requests.

Even though a follower can lag behind the leader, it will always
receive new updates in the same order as the leader. For example,
suppose one client only ever queries follower 1, and another only
ever queries follower 2. In that case, the two clients will see the
state evolving at different times, as followers are not perfectly in
sync.

The consistency model that ensures operations occur in the same
order for all observers, but doesn’t provide any real-time guarantee about when an operation’s side-effect becomes visible to them,
is called sequential consistency. The lack of real-time guarantees is what differentiates sequential consistency from linearizability.

A producer/consumer system synchronized with a queue is an example of this model; a producer writes items to the queue, which
a consumer reads. The producer and the consumer see the items
in the same order, but the consumer lags behind the producer.

### Eventual consistency
Although we managed to increase the read throughput, we had to
pin clients to followers — if a follower becomes unavailable, the
client loses access to the store. We could increase the availability
by allowing the client to query any follower. But this comes at a
steep price in terms of consistency. For example, say there are two
followers, 1 and 2, where follower 2 lags behind follower 1. If a
client queries follower 1 and then follower 2, it will see an earlier
state, which can be very confusing. The only guarantee the client has is that eventually all followers will converge to the final state if
writes to the system stop. This consistency model is called *eventual
consistency*.

It’s challenging to build applications on top of an eventually consistent data store because the behavior is different from what we
are used to when writing single-threaded applications. As a result,
subtle bugs can creep up that are hard to debug and reproduce.
Yet, in eventual consistency’s defense, not all applications require
linearizability. For example, an eventually consistent store is perfectly fine if we want to keep track of the number of users visiting
a website, since it doesn’t really matter if a read returns a number
that is slightly out of date.

### The CAP theorem
When a network partition happens, parts of the system become
disconnected from each other. For example, some clients might
no longer be able to reach the leader. The system has two choices
when this happens; it can either:
* remain available by allowing clients to query followers that
are reachable, sacrificing strong consistency;
* or guarantee strong consistency by failing reads that can’t
reach the leader.

This concept is expressed by the CAP theorem, which can be sum-
marized as: “strong consistency, availability and partition tolerance: pick two out of three.” In reality, the choice really is only
between strong consistency and availability, as network faults are
a given and can’t be avoided.

Confusingly enough, the CAP theorem’s definition of availability
requires that every request eventually receives a response. But in
real systems, achieving perfect availability is impossible. Moreover, a very slow response is just as bad as one that never occurs.
So, in other words, many highly-available systems can’t be considered available as defined by the CAP theorem. Similarly, the
theorem’s definition of consistency and partition tolerance is very
precise, limiting its practical applications. A more useful way to
think about the relationship between availability and consistency
is as a spectrum. And so, for example, a strongly consistent and
partition-tolerant system as defined by the CAP theorem occupies
just one point in that spectrum.

Also, even though network partitions can happen, they are usually
rare within a data center. But, even in the absence of a network partition, there is a tradeoff between consistency and latency (or performance). The stronger the consistency guarantee is, the higher
the latency of individual operations must be. This relationship is
expressed by the **PACELC theorem**, an extension to the CAP theorem. It states that in case of network partitioning (P), one has to
choose between availability (A) and consistency (C), but else (E),
even when the system is running normally in the absence of partitions, one has to choose between latency (L) and consistency (C). In
practice, the choice between latency and consistency is not binary
but rather a spectrum.

This is why some off-the-shelf distributed data stores come with
counter-intuitive consistency guarantees in order to provide high
availability and performance. Others have knobs that allow you
to choose whether you want better performance or stronger consistency guarantees, like Azure’s Cosmos DB and Cassandra.

Another way to interpret the PACELC theorem is that there is a
tradeoff between the amount of coordination required and performance. One way to design around this fundamental limitation is to move coordination away from the critical path. For example,
earlier we discussed that for a read to be strongly consistent, the
leader has to contact a majority of followers. That coordination tax
is paid for each read!

## Chain replication
Chain replication is a widely used replication protocol that uses
a very different topology from leader-based replication protocols
like Raft. In chain replication, processes are arranged in a chain.
The leftmost process is referred to as the chain’s *head*, while the
rightmost one is the chain’s *tail*.

Clients send writes exclusively to the head, which updates its local state and forwards the update to the next process in the chain.
Similarly, that process updates its state and forwards the change
to its successor until it eventually reaches the tail. 

When the tail receives an update, it applies it locally and sends
an acknowledgment to its predecessor to signal that the change
has been committed. The acknowledgment flows back to the head,
which can then reply to the client that the write succeeded.

Client reads are served exclusively by the tail.
In the absence of failures, the protocol is strongly consistent as all
writes and reads are processed one at a time by the tail. But what
happens if a process in the chain fails?

Fault tolerance is delegated to a dedicated component, the configuration manager or *control plane*. At a high level, the control plane
monitors the chain’s health, and when it detects a faulty process, it
removes it from the chain. The control plane ensures that there is a single view of the chain’s topology that every process agrees with.
For this to work, the control plane needs to be fault-tolerant, which
requires state machine replication (e.g., Raft). So while the chain
can tolerate up to N − 1 processes failing, where N is the chain’s
length, the control plane can only tolerate 𝐶/2 failures, where C is
the number of replicas that make up the control plane.

There are three failure modes in chain replication: the head can
fail, the tail can fail, or an intermediate process can fail. If the head
fails, the control plane removes it by reconfiguring its successor to
be the new head and notifying clients of the change. If the head
committed a write to its local state but crashed before forwarding it
downstream, no harm is done. Since the write didn’t reach the tail,
the client that issued it hasn’t received an acknowledgment for it
yet. From the client’s perspective, it’s just a request that timed out
and needs to be retried. Similarly, no other client will have seen
the write’s side effects since it never reached the tail.

If the tail fails, the control plane removes it and makes its predecessor the chain’s new tail. Because all updates that the tail has
received must necessarily have been received by the predecessor
as well, everything works as expected.

If an intermediate process X fails, the control plane has to link X’s
predecessor with X’s successor. This case is a bit trickier to handle since X might have applied some updates locally but failed before
forwarding them to its successor. Therefore, X’s successor needs
to communicate to the control plane the sequence number of the
last committed update it has seen, which is then passed to X’s predecessor to send the missing updates downstream.

Chain replication can tolerate up to N − 1 failures. So, as more
processes in the chain fail, it can tolerate fewer failures. This is why
it’s important to replace a failing process with a new one. This can
be accomplished by making the new process the tail of the chain
after syncing it with its predecessor.

The beauty of chain replication is that there are only a handful of
simple failure modes to consider. That’s because for a write to
commit, it needs to reach the tail, and consequently, it must have
been processed by every process in the chain. This is very different
from a quorum-based replication protocol like Raft, where only a
subset of replicas may have seen a committed write.

Chain replication is simpler to understand and more performant
than leader-based replication since the leader’s job of serving client
requests is split among the head and the tail. The head sequences
writes by updating its local state and forwarding updates to its successor. Reads, however, are served by the tail, and are interleaved
with updates received from its predecessor. Unlike in Raft, a read
request from a client can be served immediately from the tail’s local state without contacting the other replicas first, which allows
for higher throughputs and lower response times.

However, there is a price to pay in terms of write latency. Since
an update needs to go through all the processes in the chain before it can be considered committed, a single slow replica can slow
down all writes. In contrast, in Raft, the leader only has to wait for
a majority of processes to reply and therefore is more resilient to
transient degradations. Additionally, if a process isn’t available,
chain replication can’t commit writes until the control plane detects the problem and takes the failing process out of the chain. In
Raft instead, a single process failing doesn’t stop writes from being committed since only a quorum of processes is needed to make progress.

That said, chain replication allows write requests to be pipelined,
which can significantly improve throughput. Moreover, read
throughput can be further increased by distributing reads across
replicas while still guaranteeing linearizability. The idea is for
replicas to store multiple versions of an object, each including
a version number and a dirty flag. Replicas mark an update
as dirty as it propagates from the head to the tail. Once the
tail receives it, it’s considered committed, and the tail sends an
acknowledgment back along the chain. When a replica receives
an acknowledgment, it marks the corresponding version as clean.
Now, when a replica receives a read request for an object, it will
immediately serve it if the latest version is clean. If not, it first
contacts the tail to request the latest committed version.

A leader introduces a scalability bottleneck. But in chain replication, the data plane (i.e., the part of the
system that handles individual client requests on the critical path)
doesn’t need a leader to do its job since it’s not concerned with
failures — its sole focus is throughput and efficiency. On the contrary, the control plane needs a leader to implement state machine
replication, but that’s required exclusively to handle the occasional
failure and doesn’t affect client requests on the critical path. Another way to think about this is that chain replication reduces the
amount of coordination needed for each client request. In turn,
this increases the data plane’s capacity to handle load. For this
reason, splitting the data plane from the control plane (i.e., the configuration management part) is a common pattern in distributed
systems.
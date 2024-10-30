# TCP/IP

## Link layer
Network protocols that operate on lo-
cal network links, like Ethernet or Wi-Fi, and provides an interface to the underlying network hardware. Switches operate at this layer and forward Ethernet packets based on their
destination MAC address. 

## Internet layer
routes packets from one machine to another
across the network. The Internet Protocol (IP) is the core protocol of this layer, which delivers packets on a best-effort basis (i.e., packets can be dropped, duplicated, or corrupted).
Routers operate at this layer and forward IP packets to the
next router along the path to their final destination.

Data sent from one machine to another it is sent in the form of IP packets. Think of IP packets as fundamental unit of data stored in bytes. 
Two main sections: IP header and IP version.
IP header: information about the packet:
- source IP address
- destination IP address
- packet size
- IP version - IPv4, IPv6

The rest of the IP packet is data. 

## Transport layer
Transmits data between two processes. To
enable multiple processes hosted on the same machine to
communicate at the same time, port numbers are used to address the processes on either end. The most important protocol in this layer is the Transmission Control Protocol (TCP),
which creates a reliable communication channel on top of IP.

We need to create a TCP connection and this process of initially setting up a connection is called handshake.  

## Application layer
Defines high-level communication protocols, like HTTP or DNS. Typically your applications will target this level of abstraction.

# Reliable links

IP doesn’t guarantee that data sent over the internet will
arrive at its destination. A transport-layer protocol that exposes a reliable communication channel between two processes on top of IP. TCP guarantees
that a stream of bytes arrives in order without gaps, duplication,
or corruption.

## Reliability
To create the illusion of a reliable channel, TCP partitions a byte
stream into discrete packets called segments. The segments are
sequentially numbered, which allows the receiver to detect holes
and duplicates. Every segment sent needs to be acknowledged
by the receiver. When that doesn’t happen, a timer fires on the
sending side and the segment is retransmitted. To ensure that the
data hasn’t been corrupted in transit, the receiver uses a checksum
to verify the integrity of a delivered segment.

## Connection lifecycle
A connection needs to be opened before any data can be transmitted on a TCP channel. The operating system manages the connection state on both ends through a socket. The socket keeps track of
the state changes of the connection during its lifetime. At a high
level, there are three states the connection can be in:
- The opening state in which the connection is being created.
- The established state in which the connection is open and
data is being transferred.
- The closing state in which the connection is being closed.

In reality, this is a simplification, as there are more states than the
three above.

A server must be listening for connection requests from clients before a connection is established. TCP uses a three-way handshake
to create a new connection.
1. The sender picks a random sequence number x and sends a
SYN segment to the receiver.
2. The receiver increments x, chooses a random sequence number y, and sends back a SYN/ACK segment.
3. The sender increments both sequence numbers and replies
with an ACK segment and the first bytes of application data.

The handshake introduces a full round-trip in which no application data is sent. So until the connection has been opened, the
bandwidth is essentially zero. The lower the round trip time is,
the faster the connection can be established. Therefore, putting
servers closer to the clients helps reduce this cold-start penalty.

After the data transmission is complete, the connection needs
to be closed to release all resources on both ends. This termination phase involves multiple round-trips. If it’s likely that
another transmission will occur soon, it makes sense to keep the
connection open to avoid paying the cold-start tax again.

Moreover, closing a socket doesn’t dispose of it immediately as it transitions to a waiting state (TIME_WAIT) that lasts several min-
utes and discards any segments received during the wait. The
wait prevents delayed segments from a closed connection from be-
ing considered part of a new connection. But if many connections
open and close quickly, the number of sockets in the waiting state
will continue to increase until it reaches the maximum number of
sockets that can be open, causing new connection attempts to fail.
This is another reason why processes typically maintain connec-
tion pools to avoid recreating connections repeatedly.

## FLow control

Flow control is a backoff mechanism that TCP implements to
prevent the sender from overwhelming the receiver. The receiver
stores incoming TCP segments waiting to be processed by the
application into a receive buffer. The receiver also communicates the size of the buffer to the sender
whenever it acknowledges a segment. Assuming it’s respecting the protocol, the sender avoids sending
more data than can fit in the receiver’s buffer. This mechanism is not too dissimilar to rate-limiting at the service
level.

## Congestion control
TCP guards not only against overwhelming the receiver, but also
against flooding the underlying network. The sender maintains
a so-called congestion window, which represents the total number
of outstanding segments that can be sent without an acknowledgment from the other side. The smaller the congestion window is,
the fewer bytes can be in flight at any given time, and the less bandwidth is utilized.

When a new connection is established, the size of the congestion
window is set to a system default. Then, for every segment acknowledged, the window increases its size exponentially until it
reaches an upper limit. This means we can’t use the network’s full
capacity right after a connection is established. The shorter the
round-trip time (RTT), the quicker the sender can start utilizing
the underlying network’s bandwidth.

What happens if a segment is lost? When the sender detects a
missed acknowledgment through a timeout, a mechanism called
congestion avoidance kicks in, and the congestion window size is
reduced. From there onwards, the passing of time increases the
window size by a certain amount, and timeouts decrease it by another.

As mentioned earlier, the size of the congestion window defines
the maximum number of bytes that can be sent without receiving an acknowledgment. Because the sender needs to wait for a full
round trip to get an acknowledgment, we can derive the maximum
theoretical bandwidth by dividing the size of the congestion win-
dow by the round trip time:

> Bandwidth = WinSize / RTT

The equation5 shows that bandwidth is a function of latency. TCP
will try very hard to optimize the window size since it can’t do
anything about the round-trip time. However, that doesn’t always
yield the optimal configuration. Due to the way congestion control
works, the shorter the round-trip time, the better the underlying
network’s bandwidth is utilized. This is more reason to put servers
geographically close to the clients.

## Custom protocols
TCP’s reliability and stability come at the price of lower bandwidth and higher latencies than the underlying network can
deliver. If we drop the stability and reliability mechanisms that
TCP provides, what we get is a simple protocol named User Datagram Protocol (UDP) — a connectionless transport layer
protocol that can be used as an alternative to TCP.

Unlike TCP, UDP does not expose the abstraction of a byte stream
to its clients. As a result, clients can only send discrete packets
with a limited size called datagrams. UDP doesn’t offer any reliability as datagrams don’t have sequence numbers and are not ac-
knowledged. UDP doesn’t implement flow and congestion control
either. Overall, UDP is a lean and bare-bones protocol. It’s used
to bootstrap custom protocols, which provide some, but not all, of
the stability and reliability guarantees that TCP does.

For example, in multiplayer games, clients sample gamepad
events several times per second and send them to a server that
keeps track of the global game state. Similarly, the server samples
the game state several times per second and sends these snapshots
back to the clients. If a snapshot is lost in transmission, there is
no value in retransmitting it as the game evolves in real-time; by
the time the retransmitted snapshot would get to the destination,
it would be obsolete. This is a use case where UDP shines; in
contrast, TCP would attempt to redeliver the missing data and
degrade the game’s experience.

# Secure links

We can use the Transport Layer Security (TLS)
protocol. TLS runs on top of TCP and encrypts the communication channel so that application layer protocols, like HTTP, can
leverage it to communicate securely. In a nutshell, TLS provides
encryption, authentication, and integrity.

## Encryption

Encryption guarantees that the data transmitted between a client
and a server is obfuscated and can only be read by the communicating processes. When the TLS connection is first opened, the client and the server
negotiate a shared encryption secret using asymmetric encryption. 

Although asymmetric encryption is slow and expensive, it’s only
used to create the shared encryption key. After that, symmetric encryption is used, which is fast and cheap. The shared key is periodically renegotiated to minimize the amount of data that can be
deciphered if the shared key is broken. 

Encrypting in-flight data has a CPU penalty, but it’s negligible
since modern processors have dedicated cryptographic instructions. Therefore, TLS should be used for all communications,
even those not going through the public internet.

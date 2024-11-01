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
and a server is **obfuscated** and can only be read by the communicating processes. When the TLS connection is first opened, the client and the server
negotiate a shared encryption secret using asymmetric encryption. 

Although asymmetric encryption is slow and expensive, it’s only
used to create the **shared encryption key**. After that, symmetric encryption is used, which is fast and cheap. The shared key is periodically renegotiated to minimize the amount of data that can be
deciphered if the shared key is broken. 

Encrypting in-flight data has a CPU penalty, but it’s negligible
since modern processors have dedicated cryptographic instructions. Therefore, TLS should be used for all communications,
even those not going through the public internet.

## Authentication

Although we have a way to obfuscate data transmitted across the
wire, the client still needs to authenticate the server to verify it’s
who it claims to be. Similarly, the server might want to authenticate the identity of the client.

TLS implements authentication using digital signatures based on
asymmetric cryptography. The server generates a key pair with a
private and a public key and shares its public key with the client.
When the server sends a message to the client, it signs it with its
private key. The client uses the server’s public key to verify that
the digital signature was actually signed with the private key. This
is possible thanks to mathematical properties3 of the key pair.

The problem with this approach is that the client has no idea
whether the public key shared by the server is authentic. Hence,
the protocol uses certificates to prove the ownership of a public
key. A certificate includes information about the owning entity,
expiration date, public key, and a digital signature of the third-party entity that issued the certificate. The certificate’s issuing entity is called a certificate authority (CA), which is also represented
with a certificate. This creates a chain of certificates that ends with
a certificate issued by a root CA, which
self-signs its certificate.

For a TLS certificate to be trusted by a device, the certificate, or one
of its ancestors, must be present in the trusted store of the client.
Trusted root CAs, such as Let’s Encrypt, are typically included in
the client’s trusted store by default by the operating system vendor.

When a TLS connection is opened, the server sends the full certificate chain to the client, starting with the server’s certificate and ending with the root CA. The client verifies the server’s certificate
by scanning the certificate chain until it finds a certificate that it
trusts. Then, the certificates are verified in reverse order from that
point in the chain. The verification checks several things, like the
certificate’s expiration date and whether the digital signature was
actually signed by the issuing CA. If the verification reaches the
last certificate in the path (the server’s own certificate) without errors, the path is verified, and the server is authenticated.

One of the most common mistakes when using TLS is letting a
certificate expire. When that happens, the client won’t be able to
verify the server’s identity, and opening a connection to the remote process will fail. This can bring an entire application down
as clients can no longer connect with it. For this reason, automation to monitor and auto-renew certificates close to expiration is
well worth the investment.

Encryption can generally be applied at different levels. These include:
- **encryption-at-rest** - data is stored in an encrypted form to prevent unauthorized access. An example would be hard drive encryption. Often managed by the data storage provider. They might handle the encryption keys, which can be accessed internally by authorized personnel.
- **encryption-in-transit** - data that is transmitted is encrypted before transmission and decrypted after reception to prevent unauthorized access during the transmission. TLS applies encryption-in-transit.
- **end-to-end encryption** - encrypts data from the true sender to the final recipient such that no other party can access the data. The encryption keys are only available to the sender and receiver, and they have no visibility of each other's keys. Popular in messaging apps, secure emails, and services that prioritize privacy.

### Public Key Infrastructure
A public key infrastructure (PKI) comprises roles and processes responsible for the management of digital certificates. This include the distribution, creation, and revocation of certificates. 

In public key cryptography, the encryption key is different from the decryption kay, which is why it is also called assymetric encryption. Each participant owns a key pair consistng of a public key that is used for encryption, and a private key or secret key that is used for decryption.

### Certificates 
The purpose of certificates is to bind public key to an identity. This proves the identity of the public key owner.

The certificate contains information about the subject Most importantly the **Common Name**, which is the domain name the public key belongs to. Additionally, each certificate has an expiry date and needs to be renewed belore it expires to remain valic.

This certificate ensures that when we encrypt a message with the public key, only the server will be able to decrypt it. 

### Certificate Authorities

Certificate authorities (CAs) are entities that are explicitly allowed to issue certificates. They do this by cryptographically signing a certificate. The identity of the CA is proven by a **CA Certificate**. Just like any other cerfificate, CA certificates are signed by another CA. This continues until a root CA is reached. The chain from the root CA to the end-user's certificate is called the **certificate chain**. The root CA's identy is checed against a hardcoded set of trusted CAs in the so-called **certaicate store** to prevent forgery of root CA certificates.

### OpenSSL
OpenSSL is a robust, open-source toolkit that implements the Secure Sockets Layer (SSL) and Transport Layer Security (TLS) protocols, as well as a powerful library for a wide variety of cryptographic functions. It is widely used to secure data in transit (such as HTTPS connections) and to perform various cryptographic tasks, like encryption, decryption, and key generation.

## Integrity
Even if the data is obfuscated, a middleman could still tamper
with it; for example, random bits within the messages could be
swapped. To protect against tampering, TLS verifies the integrity
of the data by calculating a message digest. A secure hash function
is used to create a message authentication code (HMAC). When a
process receives a message, it recomputes the digest of the message
and checks whether it matches the digest included in the message.
If not, then the message has either been corrupted during transmission or has been tampered with. In this case, the message is
dropped.

The TLS HMAC protects against data corruption as well, not just
tampering. You might be wondering how data can be corrupted if
TCP is supposed to guarantee its integrity. While TCP does use a
checksum to protect against data corruption, it’s not 100% reliable: it fails to detect errors for roughly 1 in 16 million to 10 billion pack-
ets. With packets of 1 KB, this is expected to happen once per 16
GB to 10 TB transmitted.

## Handshake
When a new TLS connection is established, a handshake between
the client and server occurs during which:

1. The parties agree on the cipher suite to use. A cipher suite
specifies the different algorithms that the client and the
server intend to use to create a secure channel, like the:
   *  key exchange algorithm used to generate shared
secrets;
   *  signature algorithm used to sign certificates;
   *  symmetric encryption algorithm used to encrypt the application data;
   *  HMAC algorithm used to guarantee the integrity and
authenticity of the application data.

2. The parties use the key exchange algorithm to create a shared
secret. The symmetric encryption algorithm uses the shared
secret to encrypt communication on the secure channel going
forward.
3. The client verifies the certificate provided by the server. The
verification process confirms that the server is who it says it
is. If the verification is successful, the client can start sending encrypted application data to the server. The server can
optionally also verify the client certificate if one is available.
These operations don’t necessarily happen in this order, as modern
implementations use several optimizations to reduce round trips.
For example, the handshake typically requires 2 round trips with
TLS 1.2 and just one with TLS 1.3. The bottom line is that creating a
new connection is not free: yet another reason to put your servers
geographically closer to the clients and reuse connections when
possible.

# Discovery
To create a new connection with a remote process, we must
first discover its IP address somehow. The most common way of
doing that is via the phone book of the internet: the Domain Name
System (DNS) — a distributed, hierarchical, and eventually con-
sistent key-value store.

When
you enter a URL in your browser, the first step is to resolve the
hostname’s IP address, which is then used to open a new TLS connection.
DNS resolution:
1. The browser checks its local cache to see whether it has resolved the hostname before. If so, it returns the cached IP
address; otherwise, it routes the request to a DNS resolver, a server typically hosted by your Internet Service Provider (ISP).

2. The resolver is responsible for iteratively resolving the hostname for its clients. The reason why it’s iterative will become
obvious in a moment. The resolver first checks its local cache
for a cached entry, and if one is found, it’s returned to the
client. If not, the query is sent to a root name server (root NS).

3. The root name server maps the top-level domain (TLD) of the
request, i.e., .com, to the address of the name server responsible for it.
The resolver sends a resolution request for example.com to the
TLD name server.
The TLD name server maps the example.com domain name to
the address of the authoritative name server responsible for the
domain.
Finally, the resolver queries the authoritative name server for
www.example.com, which returns the IP address of the www
hostname.

If the query included a subdomain of example.com, like
news.example.com, the authoritative name server would have
returned the address of the name server responsible for the
subdomain, and an additional request would be required.

The original DNS protocol sent plain-text messages primarily over
UDP for efficiency reasons. However, because this allows any-
one monitoring the transmission to snoop, the industry has mostly
moved to secure alternatives, such as DNS on top of TLS.

The resolution process involves several round trips in the worst
case, but its beauty is that the address of a root name server is
all that’s needed to resolve a hostname. That said, the resolution
would be slow if every request had to go through several name server lookups. Not only that, but think of the scale required for
the name servers to handle the global resolution load. So caching
is used to speed up the resolution process since the mapping of domain names to IP addresses doesn’t change often — the browser,
operating system, and DNS resolver all use caches internally.

How do these caches know when to expire a record? Every DNS
record has a time to live (TTL) that informs the cache how long the
entry is valid for. But there is no guarantee that clients play nicely
and enforce the TTL. So don’t be surprised when you change a
DNS entry and find out that a small number of clients are still trying to connect to the old address long after the TTL has expired.

Setting a TTL requires making a tradeoff. If you use a long TTL,
many clients won’t see a change for a long time. But if you set it too
short, you increase the load on the name servers and the average
response time of requests because clients will have to resolve the
hostname more often.

If your name server becomes unavailable for any reason, then the smaller the record’s TTL is, the higher the number of clients impacted will be. DNS can easily become a single point of failure —
if your DNS name server is down and clients can’t find the IP address of your application, they won’t be able to connect it. This can
lead to massive outages.
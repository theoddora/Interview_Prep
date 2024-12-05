# TCP/IP
What is it? The TCP/IP model is a fundamental framework for computer networking. It stands for Transmission Control Protocol/Internet Protocol, which are the core protocols of the Internet. This model defines how data is transmitted over networks, ensuring reliable communication between devices. It consists of four layers: the Link Layer, the Internet Layer, the Transport Layer, and the Application Layer. Each layer has specific functions that help manage different aspects of network communication, making it essential for understanding and working with modern networks.

## Link layer
Network protocols that operate on local network links, like Ethernet or Wi-Fi, and provides an interface to the underlying network hardware. Switches operate at this layer and forward Ethernet packets based on their
destination MAC address. 

## Internet layer
Routes packets from one machine to another
across the network. The Internet Protocol (IP) is the core protocol of this layer, which delivers packets on a **best-effort basis** (i.e., packets can be dropped, duplicated, or corrupted).
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

We need to create a **TCP connection** and this process of initially setting up a connection is called handshake. 

## Application layer
Defines high-level communication protocols, like HTTP or DNS. Typically your applications will target this level of abstraction.

![ ](/Resources/images/osi.png)

# Reliable links
At the internet layer, the communication between two nodes 
happens by routing packets to their destination from one router to the
next. Two ingredients are required for this: a way to address nodes
and a mechanism to route packets across routers.

Addressing is handled by the IP protocol. To decide
where to send a packet, a router needs to consult a local routing
table. The table maps a destination address to the address of the
next router along the path to that destination. The responsibility
of building and communicating the routing tables across routers
lies with the Border Gateway Protocol (BGP).

IP doesn’t guarantee that data sent over the internet will
arrive at its destination. For example, if a router becomes overloaded, it might start dropping packets. TCP comes
in, a transport-layer protocol that exposes a reliable communication channel between two processes on top of IP. TCP guarantees
that a stream of bytes arrives in order without gaps, duplication,
or corruption. TCP also implements a set of *stability* patterns to avoid overwhelming the network and the receiver.

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

Moreover, closing a socket doesn’t dispose of it immediately as it transitions to a waiting state (TIME_WAIT) that lasts several 
minutes and discards any segments received during the wait. The
wait prevents delayed segments from a closed connection from being considered part of a new connection. But if many connections
open and close quickly, the number of sockets in the waiting state
will continue to increase until it reaches the maximum number of
sockets that can be open, causing new connection attempts to fail.
This is another reason why processes typically maintain connection pools to avoid recreating connections repeatedly.

## Flow control

Flow control is a backoff mechanism that TCP implements to
prevent the sender from overwhelming the receiver. The receiver
stores incoming TCP segments waiting to be processed by the
application into a receive buffer. The receiver also communicates the size of the buffer to the sender
whenever it acknowledges a segment. Assuming it’s respecting the protocol, the sender avoids sending
more data than can fit in the receiver’s buffer. This mechanism is not too dissimilar to rate-limiting at the service
level, a mechanism that rejects a request when a specific quota is
exceeded. But, rather than rate-limiting on an
API key or IP address, TCP is rate-limiting on a connection level.

## Congestion control
TCP guards not only against overwhelming the receiver, but also
against flooding the underlying network. The sender maintains
a so-called *congestion window*, which represents the total number
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
*congestion avoidance* kicks in, and the congestion window size is
reduced. From there onwards, the passing of time increases the
window size by a certain amount, and timeouts decrease it by another.

As mentioned earlier, the size of the congestion window defines
the maximum number of bytes that can be sent without receiving an acknowledgment. Because the sender needs to wait for a full
round trip to get an acknowledgment, we can derive the maximum
theoretical bandwidth by dividing the size of the congestion window by the round trip time:

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
with a limited size called *datagrams*. UDP doesn’t offer any reliability 
as datagrams don’t have sequence numbers and are not acknowledged. 
UDP doesn’t implement flow and congestion control
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


| Feature                | TCP                                                   | UDP                              |
|------------------------|-------------------------------------------------------|----------------------------------|
| **Connection Type**    | Requires a three-way handshake before data transfer, adding latency. | Connectionless; data is sent immediately. |
| **Reliability**        | Ensures reliable delivery with acknowledgments, retransmissions, and in-order delivery. | No reliability; packets may be lost or arrive out of order. |
| **Flow Control**       | Uses a sliding window mechanism to manage data flow and avoid overwhelming the receiver. | No flow control; sends data regardless of receiver state. |
| **Congestion Control** | Adjusts transmission speed based on network conditions to prevent congestion. | No congestion control; data is sent at a constant rate. |
| **Header Size**        | Larger (minimum 20 bytes) due to fields for reliability and control. | Smaller (8 bytes), reducing overhead. |
| **Speed**              | Slower due to additional features ensuring reliability. | Faster because it prioritizes speed over reliability. |

### Summary
- **TCP** is used when reliability, order, and error correction are critical (e.g., file transfers, web browsing, email).
- **UDP** is preferred for real-time applications where speed is more important than reliability (e.g., video streaming, online gaming, VoIP).


# Secure links

We can use the *Transport Layer Security* (TLS)
protocol. TLS runs on top of TCP and encrypts the communication channel so that application layer protocols, like HTTP, can
leverage it to communicate securely. In a nutshell, TLS provides
*encryption*, *authentication*, and *integrity*.

## Encryption

Encryption guarantees that the data transmitted between a client
and a server is **obfuscated** and can only be read by the communicating processes. 
When the TLS connection is first opened, the client and the server
negotiate a shared encryption secret using asymmetric encryption. 

Although asymmetric encryption is slow and expensive, it’s only
used to create the **shared encryption key**. After that, symmetric encryption 
is used, which is fast and cheap. The shared key is periodically renegotiated to minimize the amount of data that can be
deciphered if the shared key is broken. 

Encrypting in-flight data has a CPU penalty, but it’s negligible
since modern processors have dedicated cryptographic instructions. Therefore, TLS should be used for all communications,
even those not going through the public internet.

Encryption can generally be applied at different levels. These include:
- **encryption-at-rest** - data is stored in an encrypted form to prevent unauthorized access. An example would be hard drive encryption. Often managed by the data storage provider. They might handle the encryption keys, which can be accessed internally by authorized personnel.
- **encryption-in-transit** - data that is transmitted is encrypted before transmission and decrypted after reception to prevent unauthorized access during the transmission. TLS applies encryption-in-transit.
- **end-to-end encryption** - encrypts data from the true sender to the final recipient such that no other party can access the data. The encryption keys are only available to the sender and receiver, and they have no visibility of each other's keys. Popular in messaging apps, secure emails, and services that prioritize privacy.

## Authentication

Although we have a way to obfuscate data transmitted across the
wire, the client still needs to authenticate the server to verify it’s
who it claims to be. Similarly, the server might want to authenticate the identity of the client.

TLS implements authentication using digital signatures based on
*asymmetric cryptography*. The server generates a key pair with a
private and a public key and shares its public key with the client.
When the server sends a message to the client, it signs it with its
private key. The client uses the server’s public key to verify that
the digital signature was actually signed with the private key. This
is possible thanks to mathematical properties of the key pair.

The problem with this approach is that the client has no idea
whether the public key shared by the server is authentic. Hence,
the protocol uses certificates to prove the ownership of a public
key. A certificate includes information about the owning entity,
expiration date, public key, and a digital signature of the third-party 
entity that issued the certificate. The certificate’s issuing 
entity is called a *certificate authority* (CA), which is also represented
with a certificate. This creates a chain of certificates that ends with
a certificate issued by a root CA, which
self-signs its certificate.

For a TLS certificate to be trusted by a device, the certificate, or one
of its ancestors, must be present in the trusted store of the client.
Trusted root CAs, such as Let’s Encrypt, are typically included in
the client’s trusted store by default by the operating system vendor.

When a TLS connection is opened, the server sends the full certificate chain
to the client, starting with the server’s certificate and ending with the 
root CA. The client verifies the server’s certificate
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

### Public Key Infrastructure
A public key infrastructure (PKI) comprises roles and processes responsible for the management of digital certificates. This include the distribution, creation, and revocation of certificates. 

In public key cryptography, the encryption key is different from the decryption kay, which is why it is also called assymetric encryption. Each participant owns a key pair consistng of a public key that is used for encryption, and a private key or secret key that is used for decryption.

### Certificates 
The purpose of certificates is to bind public key to an identity. This proves the identity of the public key owner.

The certificate contains information about the subject. Most importantly the **Common Name**, which is the domain name the public key belongs to. Additionally, each certificate has an expiry date and needs to be renewed belore it expires to remain valid.

This certificate ensures that when we encrypt a message with the public key, only the server will be able to decrypt it. 

### Certificate Authorities

Certificate authorities (CAs) are entities that are explicitly allowed to issue certificates. They do this by cryptographically signing a certificate. The identity of the CA is proven by a **CA Certificate**. Just like any other cerfificate, CA certificates are signed by another CA. This continues until a root CA is reached. The chain from the root CA to the end-user's certificate is called the **certificate chain**. The root CA's identityy is checked against a hardcoded set of trusted CAs in the so-called **certaicate store** to prevent forgery of root CA certificates.

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
If not, then the message has either been corrupted during transmission 
or has been tampered with. In this case, the message is
dropped.

The TLS HMAC protects against data corruption as well, not just
tampering. You might be wondering how data can be corrupted if
TCP is supposed to guarantee its integrity. While TCP does use a
checksum to protect against data corruption, it’s not 100% reliable: 
it fails to detect errors for roughly 1 in 16 million to 10 billion 
packets. With packets of 1 KB, this is expected to happen once per 16
GB to 10 TB transmitted.

## Handshake
When a new TLS connection is established, a handshake between
the client and server occurs during which:

![ ](/Resources/images/https.png)

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
is. If the verification is successful, the client can start sending 
encrypted application data to the server. The server can
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
doing that is via the phone book of the internet: the *Domain Name
System* (DNS) — a distributed, hierarchical, and eventually 
consistent key-value store.

We will look at how DNS resolution works in a
browser, but the process is similar for other types of clients. 
When you enter a URL in your browser, the first step is to resolve the
hostname’s IP address, which is then used to open a new TLS connection.

DNS resolution:
1. The browser checks its local cache to see whether it has resolved 
the hostname before. If so, it returns the cached IP
address; otherwise, it routes the request to a DNS resolver, 
a server typically hosted by your Internet Service Provider (ISP).
2. The resolver is responsible for iteratively resolving the hostname for its clients. 
The reason why it’s iterative will become
obvious in a moment. The resolver first checks its local cache
for a cached entry, and if one is found, it’s returned to the
client. If not, the query is sent to a root name server (root NS).
3. The root name server maps the *top-level domain* (TLD) of the
request, i.e., .com, to the address of the name server responsible for it.
4. The resolver sends a resolution request for example.com to the
TLD name server.
5. The TLD name server maps the example.com domain name to
the address of the *authoritative name server* responsible for the
domain.
6. Finally, the resolver queries the authoritative name server for
www.example.com, which returns the IP address of the www
hostname.

If the query included a subdomain of example.com, like
news.example.com, the authoritative name server would have
returned the address of the name server responsible for the
subdomain, and an additional request would be required.

![ ](/Resources/images/dns.png)

The original DNS protocol sent plain-text messages primarily over
UDP for efficiency reasons. However, because this allows 
anyone monitoring the transmission to snoop, the industry has mostly
moved to secure alternatives, such as DNS on top of TLS.

The resolution process involves several round trips in the worst
case, but its beauty is that the address of a root name server is
all that’s needed to resolve a hostname. That said, the resolution
would be slow if every request had to go through several name server 
lookups. Not only that, but think of the scale required for
the name servers to handle the global resolution load. So caching
is used to speed up the resolution process since the mapping of domain 
names to IP addresses doesn’t change often — the browser,
operating system, and DNS resolver all use caches internally.

How do these caches know when to expire a record? Every DNS
record has a *time to live* (TTL) that informs the cache how long the
entry is valid for. But there is no guarantee that clients play nicely
and enforce the TTL. So don’t be surprised when you change a
DNS entry and find out that a small number of clients are still trying 
to connect to the old address long after the TTL has expired.

Setting a TTL requires making a tradeoff. If you use a long TTL,
many clients won’t see a change for a long time. But if you set it too
short, you increase the load on the name servers and the average
response time of requests because clients will have to resolve the
hostname more often.

If your name server becomes unavailable for any reason, then the 
smaller the record’s TTL is, the higher the number of clients 
impacted will be. DNS can easily become a single point of failure —
if your DNS name server is down and clients can’t find the IP 
address of your application, they won’t be able to connect it. This can
lead to massive outages.

This brings us to an interesting observation. DNS could be a lot
more robust to failures if DNS caches would serve stale entries
when they can’t reach a name server, rather than treating TTLs
as time bombs. Since entries rarely change, serving a stale entry is
arguably a lot more robust than not serving any entry at all. The
principle that a system should continue to function even when a
dependency is impaired is also referred to as “static stability”;

# APIs
We want the client to invoke operations offered by the server.
To that end, the server uses an *adapter* — which defines its 
application programming interface (API) — to translate messages 
received from the communication link to interface calls implemented
by its business logic. 

The communication style between a client and a server can be 
*direct* or *indirect*, depending on whether the client communicates 
directly with the server or indirectly through a broker. Direct 
communication requires that both processes are up and running for the
communication to succeed. However, sometimes this guarantee
is either not needed or very hard to achieve, in which case indirect 
communication is a better fit. An example of indirect communication 
is *messaging*. In this model, the sender and the receiver
don’t communicate directly, but they exchange messages through
a message channel (the broker).

We will focus our attention on a direct communication style called *request-response*, in which a client sends a *request
message* to the server, and the server replies with a *response message*.
This is similar to a function call but across process boundaries and
over the network.

The request and response messages contain data that is serialized
in a language-agnostic format. The choice of format determines
a message’s serialization and deserialization speed, whether it’s
human-readable, and how hard it is to evolve it over time. A *textual* format like JSON is self-describing and human-readable, at
the expense of increased verbosity and parsing overhead. On the
other hand, a binary format like Protocol Buffers is leaner and
more performant than a textual one at the expense of human readability.

When a client sends a request to a server, it can block and wait
for the response to arrive, making the communication *synchronous*.
Alternatively, it can ask the outbound adapter to invoke a callback
when it receives the response, making the communication *asynchronous*.

Synchronous communication is inefficient, as it blocks threads
that could be used to do something else. Some languages, like
JavaScript, C#, and Go, can completely hide callbacks through
language primitives such as async/await. These primitives
make writing asynchronous code as straightforward as writing
synchronous code.

Commonly used IPC technologies for request-response interactions are HTTP and gRPC. Typically, internal APIs used for
server-to-server communications within an organization are implemented with a high-performance RPC framework like gRPC.
In contrast, external APIs available to the public tend to be based on HTTP, since web browsers can easily make HTTP requests via
JavaScript code.

A popular set of design principles for designing elegant and scalable HTTP APIs is representational state transfer (REST5), and an
API based on these principles is said to be RESTful. For example,
these principles include that:
* requests are stateless, and therefore each request contains all
the necessary information required to process it;
* responses are implicitly or explicitly labeled as cacheable or
non-cacheable. If a response is cacheable, the client can reuse
the response for a later, equivalent request.

Given the ubiquity of RESTful HTTP APIs, we will walk through
the process of creating an HTTP API.

## HTTP
HTTP is a request-response protocol used to encode and transport
information between a client and a server. In an HTTP *transaction*,
the client sends a *request message* to the server’s API endpoint, and
the server replies back with a *response message*.

In HTTP 1.1, a message is a textual block of data that contains a
start line, a set of headers, and an optional body:
* In a request message, the *start line* indicates what the request
is for, and in a response message, it indicates whether the
request was successful or not.
* The *headers* are key-value pairs with metadata that describes
the message.
* The message *body* is a container for data.

HTTP is a stateless protocol, which means that everything needed
by a server to process a request needs to be specified within the request itself, without context from previous requests. HTTP uses
TCP for the reliability guarantees. When it
runs on top of TLS, it’s also referred to as HTTPS.

HTTP 1.1 keeps a connection to a server open by default to avoid
needing to create a new one for the next transaction. However, a
new request can’t be issued until the response to the previous one
has been received (aka *head-of-line blocking* or HOL blocking); in
other words, the transactions have to be serialized. For example,
a browser that needs to fetch several images to render an HTML
page has to download them one at a time, which can be very inefficient.

Although HTTP 1.1 technically allows some type of requests to be pipelined, it still suffers from HOL blocking as a single slow response will block all the responses after it. With HTTP 1.1, the
typical way to improve the throughput of outgoing requests is by
creating multiple connections. However, this comes with a price
because connections consume resources like memory and sockets.

HTTP 2 was designed from the ground up to address the main
limitations of HTTP 1.1. It uses a binary protocol rather than a
textual one, allowing it to multiplex multiple concurrent request-response transactions (streams) on the same connection. In early
2020 about half of the most-visited websites on the internet were
using the new HTTP 2 standard.

HTTP 3 is the latest iteration of the HTTP standard, which is
based on UDP and implements its own transport protocol to
address some of TCP’s shortcomings. For example, with HTTP
2, a packet loss over the TCP connection blocks all streams (HOL),
but with HTTP 3 a packet loss interrupts only one stream, not all
of them.

## Resources
An HTTP server hosts resources, where a resource can be a physical or abstract entity, like a document, an image, or a collection
of other resources. A URL identifies a resource by describing its
location on the server.

A URL (Uniform Resource Locator) is the address of a unique resource on the internet. It is one of the key mechanisms used by browsers to retrieve published resources, such as HTML pages, CSS documents, images, and so on.

Example:  https://www.example.com:80/products?sort=price

### Scheme
The first part of the URL is the scheme, which indicates the protocol that the browser must use to request the resource. Example - HTTP, HTTPS.

### Authority
Next follows the authority, which is separated from the scheme by the character pattern ://. If present the authority includes both the domain (e.g. www.example.com) and the port (80), separated by a colon. 

* The domain indicates which Web server is being requested. Usually this is a domain name, but an IP address may also be used (but this is rare as it is much less convenient).
* The port indicates the technical "gate" used to access the resources on the web server. It is usually omitted if the web server uses the standard ports of the HTTP protocol (80 for HTTP and 443 for HTTPS) to grant access to its resources. Otherwise it is mandatory.

### Path to resource
/path/to/myfile.html is the path to the resource on the Web server. In the early days of the Web, a path like this represented a physical file location on the Web server. Nowadays, it is mostly an abstraction handled by Web servers without any physical reality.

### Parameters
Those parameters are a list of key/value pairs separated with the & symbol. The Web server can use those parameters to do extra stuff before returning the resource. 

URLs can also model relationships between resources. For example, since a product is a resource that belongs to the collection of
products, the product with the unique identifier 42 could have the
following relative URL: /products/42. And if the product also has
a list of reviews associated with it, we could append its resource
name to the product’s URL, i.e., /products/42/reviews. However, the
API becomes more complex as the nesting of resources increases,
so it’s a balancing act.

Naming resources is only one part of the equation; we also have
to serialize the resources on the wire when they are transmitted in
the body of request and response messages. When a client sends a
request to get a resource, it adds specific headers to the message to
describe the preferred representation for the resource. The server
uses these headers to pick the most appropriate representation
for the response. Generally, in HTTP APIs, JSON is used to represent non-binary resources.

## Request methods

HTTP requests can create, read, update, and delete (CRUD) resources using request *methods*. When a client makes a request to a
server for a particular resource, it specifies which method to use.
You can think of a request method as the verb or action to use on
a resource.
The most commonly used methods are POST, GET, PUT, and
DELETE. For example, the API of a catalog service could be
defined as follows:
* POST /products — Create a new product and return the URL
of the new resource.
* GET /products — Retrieve a list of products. The query string
can be used to filter, paginate, and sort the collection.
* GET /products/42 — Retrieve product 42.
* PUT /products/42 — Update product 42.
* DELETE /products/42 — Delete product 42.

Request methods can be categorized based on whether they are
safe, cachabe and whether they are idempotent. 
* A **safe** method should not
have any visible side effects and can safely be cached.
* An **idempotent** method can be executed multiple times, and the end result
should be the same as if it was executed just a single time. Idempotency is a crucial aspect of APIs.

| Method  | Safe | Idempotent | Cacheable    |
|---------|------|------------|--------------|
| GET     | Yes  | Yes        | Yes          |
| HEAD    | Yes  | Yes        | Yes          |
| OPTIONS | Yes  | Yes        | No           |
| TRACE   | Yes  | Yes        | No           |
| PUT     | No   | Yes        | No           |
| DELETE  | No   | Yes        | No           |
| POST    | No   | No         | Conditional* |
| PATCH   | No   | No         | Conditional* |
| CONNECT | No   | No         | No           |

POST and PATCH are cacheable when responses explicitly include freshness information and a matching Content-Location header.
Freshness information is provided in HTTP headers, like Cache-Control or Expires. For example:
 
> Cache-Control: max-age=3600  # Cache this response for one hour

> Content-Location: /api/users/123


### POST vs PUT

| Aspect         | POST                                         | PUT                                        |
|----------------|----------------------------------------------|--------------------------------------------|
| **Purpose**    | Create a new resource                        | Update or create a resource at a specific URI |
| **Idempotency**| No                                           | Yes                                        |
| **URI Control**| Server decides URI                           | Client provides URI                        |
| **Use Case**   | Submitting forms, adding entries             | Updating resources, replacing existing data |

In short, use POST for creating resources where the server assigns the URI, and use PUT when you want to update an existing resource or create a new one at a specified location.

### PATCH vs PUT

| Aspect         | PUT                                           | PATCH                                     |
|----------------|-----------------------------------------------|-------------------------------------------|
| **Purpose**    | Replaces an entire resource                   | Partially updates a resource              |
| **Idempotency**| Yes                                           | Yes (when implemented correctly)          |
| **Scope**      | Updates all fields (replaces the resource)    | Updates only specified fields             |
| **Use Case**   | Full update or replace                        | Partial update (e.g., changing one field) |

## Response status codes

After the server has received a request, it needs to process it and
send a response back to the client. The HTTP response contains a
*status code* to communicate to the client whether the request succeeded or not. Different status code ranges have different meanings.

Status codes between 200 and 299 are used to communicate success. For example, 200 (OK) means that the request succeeded, and
the body of the response contains the requested resource.

Status codes between 300 and 399 are used for redirection. For example, 301 (*Moved Permanently*) means that the requested resource
has been moved to a different URL specified in the response message *Location* header.

Status codes between 400 and 499 are reserved for client errors. A request that fails with a client error will usually return the same
error if it’s retried since the error is caused by an issue with the
client, not the server. Because of that, it shouldn’t be retried. Some common client errors are:
* 400 (*Bad Request*) — Validating the client-side input has
failed.
* 401 (*Unauthorized*) — The client isn’t authenticated.
* 403 (*Forbidden*) — The client is authenticated, but it’s not allowed to access the resource.
* 404 (Not Found) — The server couldn’t find the requested resource.

Status codes between 500 and 599 are reserved for server errors. A
request that fails with a server error can be retried as the issue that caused it to fail might be temporary. These are some typical server
status codes:
* 500 (*Internal Server Error*) — The server encountered an 
unexpected error that prevented it from handling the request.
* 502 (*Bad Gateway*) — The server, while acting as a gateway
or proxy, received an invalid response from a downstream
server it accessed while attempting to handle the request.
* 503 (*Service Unavailable*) — The server is currently unable to
handle the request due to a temporary overload or scheduled
maintenance.

## Open API
Now that we understand how to model an API with HTTP, we
can write an adapter that handles HTTP requests by calling the
business logic of the service. 

```java
interface CatalogService
{
List<Product> GetProducts(...);
Product GetProduct(...);
void AddProduct(...);
void DeleteProduct(...);
void UpdateProduct(...)
}
```

So when the HTTP adapter receives a GET /products request to
retrieve the list of all products, it will invoke the GetProducts(…)
method and convert the result into an HTTP response. Although
this is a simple example, you can see how the adapter connects the
IPC mechanism (HTTP) to the business logic.

We can generate a skeleton of the HTTP adapter by defining the API of the service with an *interface definition language* (IDL). An
IDL is a language-independent definition of the API that can be
used to generate boilerplate code for the server-side adapter and
client-side software development kits (SDKs) in your languages of
choice. 

The OpenAPI specification, which evolved from the Swagger
project, is one of the most popular IDLs for RESTful HTTP APIs.
With it, we can formally describe the API in a YAML document,
including the available endpoints, supported request methods,
and response status codes for each endpoint, and the schema of
the resources’ JSON representation.

## Evolution
An API starts out as a well-designed interface. Slowly but surely,
it will have to change to adapt to new use cases. The last thing we
want to do when evolving an API is to introduce a breaking change
that requires all clients to be modified at once, some of which we
might have no control over.

There are two types of changes that can break compatibility, one at the endpoint level and another at the message level. For example, if we were to change the /products endpoint to /new-products,
it would obviously break clients that haven’t been updated to support the new endpoint. The same applies when making a 
previously optional query parameter mandatory.

Changing the schema of request or response messages in a
backward-incompatible way can also wreak havoc. For example,
changing the type of the category property in the Product schema
from string to number is a breaking change that would cause the
old deserialization logic to blow up in clients. Similar arguments
can be made for messages represented with other serialization
formats, like Protocol Buffers.

REST APIs should be versioned to support breaking changes,
e.g., by prefixing a version number in the URLs (*/v1/products/*).
However, as a general rule of thumb, APIs should evolve in a
backward-compatible way unless there is a very good reason.
Although backward-compatible APIs tend not to be particularly
elegant, they are practical.

## Idempotency
When an API request times out, the client has no idea whether the
server actually received the request or not. For example, the server
could have processed the request and crashed right before sending
a response back to the client.

An effective way for clients to deal with transient failures such as
these is to retry the request one or more times until they get a response back. Some HTTP request methods (e.g., PUT, DELETE)
are considered inherently idempotent as the effect of executing
multiple identical requests is identical to executing only one request. For example, if the server processes the same PUT request for the same resource twice in a row, the end effect would be the
same as if the PUT request was executed only once.

But what about requests that are not inherently idempotent? For
example, suppose a client issues a POST request to add a new
product to the catalog service. If the request times out, the client
has no way of knowing whether the request succeeded or not. If
the request succeeds, retrying it will create two identical products,
which is not what the client intended.

In order to deal with this case, the client might have to implement
some kind of reconciliation logic that checks for duplicate products and removes them when the request is retried. You can see
how this introduces a lot of complexity for the client. Instead of
pushing this complexity to the client, a better solution would be
for the server to create the product only once by making the POST
request idempotent, so that no matter how many times that specific request is retried, it will appear as if it only executed once.

For the server to detect that a request is a duplicate, it needs to be
decorated with an idempotency key — a unique identifier (e.g., a
UUID). The identifier could be part of a header, like Idempotency-Key in Stripe’s API. For the server to detect duplicates, it needs to
remember all the request identifiers it has seen by storing them in a
database. When a request comes in, the server checks the database
to see if the request ID is already present. If it’s not there, it adds
the request identifier to the database and executes the request. Request identifiers don’t have to be stored indefinitely, and they can
be purged after some time.

Now here comes the tricky part. Suppose the server adds the request identifier to the database and crashes before executing the request. In that case, any future retry won’t have any effect because
the server will think it has already executed it. So what we really
want is for the request to be handled atomically: either the server
processes the request successfully and adds the request identifier
to the database, or it fails to process it without storing the request identifier.

If the request identifiers and the resources managed by the server
are stored in the same database, we can guarantee atomicity with
ACID transactions. In other words, we can wrap the product creation and request identifier log within the same database transaction in the POST handler. However, if the handler needs to make
external calls to other services to handle the request, the implementation becomes a lot more challenging, since it requires some
form of coordination.

Now, assuming the server can detect a duplicate request, how
should it be handled? In our example, the server could respond
to the client with a status code that signals that the product
already exists. But then the client would have to deal with this
case differently than if it had received a successful response for
the first POST request (*201 Created*). So ideally, the server should
return the same response that it would have returned for the very
first request.

When in doubt, it’s helpful to follow the principle of least astonishment.

To summarize, an idempotent API makes it a lot easier to implement clients that are robust to failures, since they can assume that
requests can be retried on failure without worrying about all the
possible edge cases.
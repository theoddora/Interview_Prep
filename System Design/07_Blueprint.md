# Load Balancing

## What is a load balancer?

As systems scale, there reaches a point where we can't use more powerful hardware (vertical scaling), so our option is to provide more nodes (horizontal scaling). Application servers can be horizontally scaled. Any time there are a variety of nodes in a cluster that can serve the same request, using a load balancer we can ensure that none of those independent nodes becomes overwhelmed.

Load balancing is the process of distributing incoming traffic across a pool of resources to ensure efficient handling of requests. In the modern world, applications are often composed of multiple resources. With high volumes of data and users, it is essential to handle requests efficiently. To achieve this, server data is often replicated to improve accessibility and ensure availability.

A load balancer is a public-facing component that accepts incoming requests and distributes them across application servers. It acts as an invisible facilitator, ensuring that application servers are utilized effectively and evenly, which helps maintain performance and prevent overloading any single server.

## Why do we load balance? What are the benefits of load balancing?

Load balancers are reverse proxies who direct user traffic to application server traffic.
Advantages include scalability, performance, security, availability.

- _Scalability_: The application can handle thousands of requests with the help of load balancers. The load balancer can route requests to many servers so that no server becomes a bottleneck. It can predict application traffic so we can add or remove service instances and utilize resources.
- _Performance_: The load balancers can distribute the traffic evenly between servers and they can also redirct traffic to servers which are geographically closer to reduce latency.
- _Security_: Load balancers also include security features - they can detect denial of service attacks where maliscios actors flood the system with many concurrent incoming requests which aim to put the system down. They can monitor traffic and block maliscious content. They can also route the traffic to firewalls for additional security.
- _Availability_: Load balancers can detect if a specific server is down and direct traffic to an available service to reduce downtime which increases the fault tolerance of the system.

## What about disadvantages of load balancing?

Load balancers add complexity to our system as they are a new component which has been introduced. Additionally, they are a single point of failure for our system - if the load balancer is down, the trafiic won't be served to the application servers.

## What are the algorithms that they use to decide where traffic goes?

Load balancers direct traffic based or policies or rules to determine which server should handle the current incoming requests. There are two types of algorithms that can help achieve these:

### Static policies

Static load balancing algorithms follow concrete rules to decide a server. They are not based on metrics of the servers and its state. Their main advantage is simplicity. But their cons are less adaptability and precision.

- Round robin: rotate requests evenly accross the server.
- Sticky round robin: same as round robin but with the addition that for some user's requests, all of his/hers requests go to the same server. This can improve performance by having related data to be on the same server. But newly arrived users are assigned randomly to a server, so uneven load can occur.
- Weighted round robin: some servers can have more priority than another. So those with higher priority can receive more traffic compared to the others. The downside is that those weights are manually configured which is less adaptive to changes.
- IP hash: Hash function accepting client IP or request url and routing evenly to servers (uniformly distributed based on the hash function properties).

### Dynamic policies

Those types of algorithms are more adaptive, because they take server conditions into account when distributing requests.

- Least connections: send requests to the server with the least amount of active connections or open requests. However, those require tracking metrics of the servers, which can be delayed if one server becomes overwhelmed or a specific request takes a lot of processing time.
- Least response time: Route requests to servers with lowest current latency or fastest response time. Latency is continuously measured to decide where to route requests. This constant monitoring, however, introduces complexity.

## What are the types of load balancing?

We can classify the load balancers based on what they check from the incoming requests.

### Application load balancing

The application load balancers check data from the request i.e. the header or session ID to redirect traffic.

#### HAProxy

HAProxy is a free, very fast and reliable reverse-proxy offering high availability, load balancing, and proxying for TCP and HTTP-based applications.

#### NGINX

It is a web server that can also be used as a reverse proxy, load balancer and HTTP cache.

#### Traefik

HTTP reverse proxy and load balancer that makes deploying microservices easy. Cloud-native.

### Network load balancers

Network load balancers check network data like the source IP address

### Global server load balancing

Global server load balancing occurs when we have geographically distributed servers.

- Akamai Global Traffic Manager - routes traffic based on geographic location and server health

### DNS load balancers

You configure your domain to route network requests accross a pool of resources on your domain.

- Cloudflare load balancing, offers DNS-based and anycast based load balancing

## Application Gateway

### Security

Input Validation
Rate Limiting / Throttling
Authorization / Authentication
Whitelist / Blacklisting
Flow Control
Authentication (OAuth 2.0)
Request Header Validations
TLS Termination
Request Deduplication
Metering / Usage data collection
Request Dispatching

## Frontend Servers

## CDN / Edge Servers

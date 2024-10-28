# Back-of-the-Envelope Math

## What is the Purpose?
One of the purposes of back-of-the-envelope math is to justify a design. 

## Types of Back-of-the-Envelope Calculations
> **QPD (Query per day)** =
[Daily active users] x
[% of active users making the query] x
[Average number of queries made by each user per day] x
[Scaling factor]

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
[Daily active users] x
[% of active users making the query to persist] x
[Average number of queries made by each user] x
[Data size per query] x
[Replication factor] x
[Time horizon]

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


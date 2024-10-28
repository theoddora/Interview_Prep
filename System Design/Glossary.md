# Glossary
> Response Time = Latency + Processing Time

**Response Time**: The time difference between the client sending the request and
receiving the response.

**Latency**: The time the request has to wait before it is processed.

**Processing Time**: The time it takes to process the request

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
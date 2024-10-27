# Understanding System Design Interview
System design is about understanding the problem you’re trying to solve before coming up with a solution. 
In a system design interview, you’re not looking to retell a design that you watched on a tech talk and read about on an engineering blog. Passing a system design interview is about having a solid understanding of the fundamentals of the building blocks and piecing them together using problem-solving skills.
You should understand how the problems are solved instead of taking the solution to the perfect answer.
When you read about a piece of technology, try to understand the big picture of the problem they’re
trying to solve and why other options were not good enough. 

# System Design Interview Framework
> Gather Requirements -> API Design ( -> Optional: QPS Calculation) -> High level Diagram -> Schema and Data structures (-> Optional: Storage Calculation) -> End to End Flow Summary -> Deep Dives

## Gather requirements
The purpose of requirement gathering is to test your ability to clarify an open-
ended and ambiguous problem statement. The interviewers want to
see if you can organize your thoughts and focus on a set of requirements. Then
you should finalize the system’s assumptions with the interviewers, so you can
focus on them for the rest of the session.

### Functional Requirement
The functional requirement gathering phase is just feature gathering.
During this section, act as a product manager and develop user stories to solve
the users’ problems. 
- Who is it for, and why do we need to build it? Globally, different users access applications as the world becomes closer
together through the internet.
- What are the features we need to solve the users’ problem? The goal here is to demonstrate your ability to think of scenarios that can break your system.

### Non-Functional Requirement
The non-functional gathering phase is critically important, and these are things that make your design unique and very engineering-focused. You should ask questions to build preliminary tuition on what could
break your system and, when it does, some areas that can be compromised to
scale for those bottleneck challenges.

#### Scale
- How Many Active Users Are There in the System? The goal of this question is to figure out the scale of the system.
- How Are the Users Distributed Across the World?
- What Are Some Scenarios That Could Lead to High QPS?
- What Are Some Scenarios That Could Lead to High Storage and Bandwidth? The goal here is to figure out what kind of pattern could cause the system to have high storage and bandwidth such that you need to scale the storage system.

### Performance Constraints
- What is the Availability and Consistency Requirement? The goal here is to discuss whether the system can tune the user product
experience’s consistency to meet the availability demand better.
- What Is the Accuracy Requirement? Similar to consistency, the goal here is to discuss whether the system can
sacrifice accuracy to meet the design constraint better.
- What Is the Response Time and Latency Constraint? The goal here is to figure out how long the users have to wait before receiving
the expected data and still deliver a good user experience.
- What Is the Freshness Requirement?
The goal here is to figure out how data staleness will impact the user experience. Data freshness categories are real-time, near-real-time, and batch processing.
- What Is the Durability Requirement? Here the goal is to figure out how data durability will impact the user
experience. In the event of a data loss, how will the user feel?

## Design API
API should be after requirement gathering because APIs are the entry point to your system. After you have the requirements, it should be clear what APIs you will need. If you try to jump into high-level diagrams or schemas right away, it can be confusing because your design might have multiple APIs.

### Purpose
The purpose of the API is to have a detailed agreement between the end-user and
the backend system. Having a detailed API contract gives you and the
interviewer confidence that you are both on the same page with the functional
requirements.

#### API Signature
You will need an API signature, input parameters, and output response to define
an API fully.

Note: You should do the back-of-the-envelope math after you finalize the API and schemas. Before you start on the math, ask the interviewer if they are interested in the math; maybe they will just tell you the QPS number. Some interviewers are disinterested in spending 5 minutes seeing you do basic algebra.
If you’re doing back of the envelope math, you're already implicitly designing for the API and the schema. How can you calculate the QPS without knowing which API the QPS is for? How do you know what storage capacity you’re calculating for without knowing the schema?

#### Input Parameter
If you
decide to introduce an input parameter because it kind of makes sense, you need
to be able to justify it if the interviewer asks you about it.

## Define High-Level Diagram
After you finish designing the API, it makes sense to start fulfilling the APIs by connecting the components.
The high-level diagram design aims to set up the foundations for the design and
give clarity to the interviewer on which parts are important to have to achieve
the requirements. In addition, having a high-level diagram gives you and the
interviewer confidence that there is at least an end-to-end flow that satisfies the
requirements.

The purpose of the high-level diagram is to bring clarity to the discussion, and
you want to be clear on the responsibility of microservice boxes.

### How to Approach High-Level Design
Starting from the top with the API and working yourself down to the
last component.

1. Step 1: Define the Client for an API
For a given API, think about who is making that API call and draw a
representation of the caller.
2. Step 2: Define the Next Sets of Logical Blocks
From the end-user, think about what the next logical block worth discussing is.
Most of the time, that may be an API gateway to take in the user request. Then
the API gateway forwards the request to an App server, and the App server sends
a write query to the database.
3. Step 3: Repeat Step 1 for the Next API


## Define Schema and Data Structure
The data model and schema can potentially significantly impact your
performance and end design. If you don’t provide detailed data models, the
interviewer can perceive the discussions as too hand-wavy.

Now that it is clear which databases, queue, in-memory, and apps you have from
the high-level diagram, you can naturally progress to providing more details on
the schema and data structures for those components. If you feel like the storage
calculation will impact your later designs, feel free to do the math after the
schema.

- Add More Detail into the Arrows
- Add More Detail into the Queue
- Add More Detail into the Database: Without the schema, the
efficiency discussion will not happen, so take a moment to discuss the schema
and its efficiency.
- Add More Detail into Cache and App Servers: 

Similar to databases, queues, cache, or any data stores, it is important to discuss
the data structure and data model because it will affect the ultimate design. So
just make sure you check any app servers you introduced that hold temporary
Situation
Design the schema for the ride rider and driver.
record to display the status of the ride to the
Don’t Do This
data or any distributed cache you introduced in your high-level design. Make
sure you present the necessary detail if it's essential to the efficiency of your
design.

## End to End Flow
Before going into deep dives, just take a moment to summarize the flow you
have to ensure there is at least a working solution that satisfies the requirements.

After your requirement, API, high-level diagram, data structure, and schema
design, the purpose of the pre-deep dive design is to take a deep breath and walk
through how each API flows through your system and whether or not they
satisfy the original requirements. It’s also a moment to begin identifying any
important talking points in the deep dive section.

## Discuss Deep Dives

### Purpose
The purpose of the deep dive section is to demonstrate to the interviewer that
you can identify areas that could be problematic—known as bottlenecks—and
develop potential solutions and trade-offs to address those issues. In addition, the
topics you bring up and how you frame your proposed solution will be telling
about your maturity as an engineer.


By this point, you should have a working design. Your job now is to identify
bottlenecks or dig deeper into components. What you choose to talk about is
very telling about your design sense. You can use back-of-the-envelope math to
justify a scalability need. Doing well in the deep dive section will set you apart
from other candidates and could lead to a more senior-level position. Ideally, you
should find 2 to 3 good solid deep dive discussions, although it’s not a hard rule,
depending on the context.

### How to Approach Deep Dive Design

Golden Question: 
> “What is the problem I am trying to solve?”

The magic formula for success is:
1. Step 1: Identify a bottleneck
1. Step 2: Come up with options
1. Step 3: Talk about the trade offs
1. Step 4: Pick one solution
1. Step 5: Active discussion with interviewer
1. Step 6: Go to step 1

The more critical bottleneck you identify, the better it will look. Of course,
your justifications from step 2 to step 4 will matter too, but if you identify
irrelevant or non-critical bottlenecks, it won’t be as impressive.

#### API and Interprocess Calls
When you have a high-level diagram, there will be boxes and arrows. For the
arrows, it’s usually an API or interprocess call. For each interprocess call, there
could potentially be interesting discussion points.

* Latency - look at your end-user API and think to yourself if
there’s a query pattern where a discussion about latency is interesting
* High QPS - Any components like servers, queue, cache, database, etc., can break if the QPS
is too high. Discussing QPS is the right time to do back-of-the-envelope
calculations to identify if QPS is an actual problem.
* Bursty of the API / Thundering Herd - However, there are always user stories in real-life patterns
that may lead to a sudden influx of requests and break the system down. Talk about scalability when such
a thundering herd event happens.
* Slow, Low Bandwidth, Congested Network - When you look at the arrow between the end-user and the system, think about
the network. The end-users may have poor bandwidth due to various reasons in
areas with poor services. For example, poor bandwidth can make photo
uploading for Instagram challenging due to insufficient bandwidth. Think about
some technical solutions and product requirement compromises that you can
make to improve the end-user experience.
* Query Optimization - Take a look at your end-user API and internal RPC calls for
the input, the output, and the API calling patterns.

#### Micro Services, Queue, and Databases
* Failure Scenario - When considering a component to discuss, think about what happens if that
component fails and how the failure impacts your non-functional requirements. Think about partial failures and complete failures and the implications and
consequences. 
* High Amount of Data - Think about whether the current query pattern will lead to too
much data and inefficiency for future queries. ill the current pattern lead to
out-of-memory issues to the app servers and the cache? Storage bottleneck is
another opportunity for back-of-the-envelope calculations to see if the current
storage pattern is sustainable and what kind of optimization solutions you can
come up with.
* Design Choices - If you’re looking at a queue, you can talk
about what kind of queue you would like to use for this question. When you dig
into possible solutions, focus on the fundamentals of the technologies, not just
buzzwords.

#### Detailed Algorithm, Data Structure, and Schema
Sometimes as you’re going through the high-level diagram, you may have only
one algorithm, one data structure, and one schema. Here’s an opportunity to
optimize the algorithm, data structure, and schema and develop more design
choices. The question you are asking yourself is,
“Do I have alternative solutions
that would make the current system even better?”

#### Concurrency
You will get some credit from identifying the concurrency issue of your design,
and it’s even better if you can come up with a reasonable solution to the
problem. So take a look at your high-level diagram and see if there are resources
that are accessed at the same time by different clients. And even if the resource
belongs to the same user, there can still be concurrency problems when there are
multiple sessions.

#### Operational Issues and Metrics
The point of this section isn’t to retell all metrics the big companies have in
place. The point is to demonstrate to the interviewer that you can build a reliable
system by identifying important areas to track.

#### Security Considerations 
In a system design interview,
while the interviewer may ask you about basic concepts such as Transport Layer
Security (TLS) and tokens as trivia questions, they shouldn’t focus on the
security discussion unless they’re significant to the requirements.
For example, you should discuss the implications of a man-in-the-middle or
malicious user attack for your design. For example, you designed an API for the
ticket booking system with book_ticket(user_id, ticket_id). What if the end-user
tries to book many tickets and cancels them later on, to lock up the tickets
maliciously? What would be the implication, and more importantly, how would
you deal with it?

### How to Frame a Solution Discussion
When you’ve identified a problem to solve, you need to come up with multiple
solutions, and for each solution, you need to discuss the trade-off. Then, after
you have fully discussed the options and trade-offs, you should try to decide
which solution you would prefer and why.

Step 1: Identify and Articulate the Problem

Step 2: Come up With Potential Solutions

Step 3: Discuss the Trade-Off

Step 4: Take a Stance on Your Preference

Step 5: Active Discussion With the Interviewer

Step 6: Return to Step 1

# Tips
1. Practice! Get hands-on with desigining real-world apps and services we use regularly (Instagram, Uber, Gmail). 
2. Study global design patterns like Load balancing, database sharding, content delivery networks, caching frequently accessed data. Know the pros/cons of different approaches  so you can intelligently weigh tradeoffs during design. When studying these patterns, anticipate the types of questions an interviewer may ask and practice responding confidenly. 
3. Get comfortable using whiteboards, diagramming apps, and other visual tools.
4. Do regular mock interviews.   

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
# Communication Tactics

## Improve public speaking
It is worth investing in public speaking techniques like
pacing, enunciation, modulation, body language, and confidence. 

## Keep the Requirements Simple
“I know Facebook uses EdgeRank to calculate each feed’s score. For now,
we’ll assume the scores are computed and stored. If we have time, we can
come back and see how we can update the scores as things change. Are you ok
with that approach?”

## Conclude and Make a Stance
“So there are option 1 and option 2 with the trade-off. I’m going to assume the
users only visit the site once a day so I will pick option 2 for this design, is the
assumption fine with you?”

## Articulate Your Thoughts
“I will use a wide-column store because the write to read ratio is extremely
high with 100k write QPS where I expect a RDBMS to not perform as well.
Also, based on the time series nature of the query, wide-column is a better fit
because of disk locality.”

## Listen to the Interviewer
“Would you like me to discuss what kind of queue I would use and why, or talk
about the scalability aspect of the queue?”

“I would use a Kafka queue because the replay capability is useful for this
streaming question in case the aggregator goes down. Should I go deeper into
scalability or is there any direction you would like me to go in regarding the
queue?"

## Show Confidence with Your Justifications
“Here are the
considerations I can think of. Should I continue to dig deeper and move on to the
next topic, or is there anything else you would like to cover?”

“Is there a direction you
would like me to head to?”

## Discussion Point With Trade-Offs
“To design for a ridesharing service, we need to update the drivers’ location.
There’s a trade-off to be made based on the frequency. The advantage of higher
frequency is more accurate data but the system will need to handle a higher
QPS and vice versa. While accuracy is important, it isn’t the end of the world
if the assigned driver isn't globally the best so we have some room. Let’s start
with 20 seconds per update and readjust if we need to.”

## Quality Over Quantity
“Above are the requirements I can think of. I am only going to focus on the
rider and driver matching part for now. If we have more time, in the end, we
can go through more requirements. I will go over the API, high-level diagram,
and deep dive into any interest areas for this core use case. Are you ok with
that?”

## Math With a Purpose
The purpose of the back-of-the-envelope calculation is to demonstrate your
ability to make reasonable assumptions and derive a result to justify a design
you’re going to make. For example, if you decide you want to start sharding the
database or introduce a cache layer, calculating the QPS and identifying the
system has a high QPS can be one of the factors to justify your desire to partition
or introduce a cache. If the QPS is low, proposing database partitioning is
introducing complexity with no benefit.

“I’ve calculated the QPS is 100k, looks like we will need to scale our app
servers since each app server I’m assuming can only take 30k QPS.”

## Focus on the Right Things
“To design an e-commerce checkout API, we need to ensure it is available and
low latency because there are studies that show low latency and availability
result in greater profit. I will focus on the signature of the API, how different
services interact with each other, and the schema of the storage layer to ensure
we meet the low latency and highly available requirements.”

## Spewing Technical Details With an Intention
“Our requirement is to have a seamless chatting experience where users should
receive the sent messages almost instantaneously. For this we have two
options, we can have the client periodically pull from the server or establish a
WebSocket connection. Since WebSocket establishes a bidirectional
connection between client and server, it allows the server to push new
messages immediately to the client. This is better than a periodic pull that
would result in a slight delay.”

## Questions to Interviewers:
1. What is the structure of the team?
2. Why are you hiring for this position?
3. What does your tech stack look like? 
4. How much of the job is working on legacy applications?
5. How many regular meetings do software engineers have to attend? 
6. Why do you like working here? 
7. What training does the company offer?
8. How often do you do a release? 
9. How do you deal with tech debt?
10. What is the team's biggest challenge?

Whenever the interviewer asks “Do you have any questions for me?”, never skip this question.

1. What is the team’s biggest challenge right now?
1. What new tech is the team experimenting with?
1. What is that one company project that you are excited about?
1. What was an interesting work the team shipped recently?
1. How do you measure the success of engineering initiatives?
1. How does the team/company celebrate wins?
1. What are some company traditions that you enjoy?

Each of the above questions covers one interesting aspect of the role and team, pick one that is most important to you. I ask one of these questions because I am interested in innovation, culture, growth, dealing with failures, and decision DNA.

Remember, it is important to ask questions in the interview for two reasons - first, it demonstrates your genuine interest in the role, position, and company; second, it allows you to get some super important insights about the role and company.
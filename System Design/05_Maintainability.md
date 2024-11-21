It’s a well-known fact that the majority of the cost of software is
spent after its initial development in maintenance activities, such
as fixing bugs, adding new features, and operating it. Thus, we
should aspire to make our systems easy to modify, extend and operate so that they are easy to maintain.

Good testing — in the form of unit, integration, and end-to-end
tests — is a minimum requirement to be able to modify or extend
a system without worrying it will break. And once a change has
been merged into the codebase, it needs to be released to production safely without affecting the application’s availability. Also,
the operators need to be able to monitor the system’s health, investigate degradations and restore the service when it gets into a bad
state. This requires altering the system’s behavior without code
changes, e.g., toggling a feature flag or scaling out a service with a
configuration change.

Historically, developers, testers, and operators were part of different teams. First, the developers handed over their software to a
team of QA engineers responsible for testing it. Then, when the
software passed that stage, it moved to an operations team respon-
sible for deploying it to production, monitoring it, and responding
to alerts. However, this model is being phased out in the industry.
Nowadays, it’s common for developers to be responsible for test-
ing and operating the software they write, which requires embrac-
ing an end-to-end view of the software’s lifecycle.

In this part, we will explore some of the best practices for testing
and operating large distributed applications.

# Testing
The longer it takes to detect a bug, the more expensive it becomes
to fix. A software test can verify that some part of the application
works as intended, catching bugs early in the process. But the real
benefit that comes from testing shows up only later when developers want to make changes to the existing implementation (e.g.,
bug fixes, refactorings, and new features) without breaking the expected behaviors. Tests also act as always up-to-date documentation and improve the quality of public interfaces since developers
have to put themselves in the users’ shoes to test them effectively.

Unfortunately, testing is not a silver bullet because it’s impossible
to predict all the states a complex distributed application can get
into. It only provides best-effort guarantees that the code being
tested is correct and fault-tolerant. No matter how exhaustive the
test coverage is, tests can only cover failures developers can imagine, not the kind of complex emergent behavior that manifests itself in production.

Although tests can’t guarantee that code is bug-free, they certainly
do a good job validating expected behaviors. So, as a rule of thumb,
if you want to be confident that your implementation behaves in
a certain way, you have to add a test for it.

## Scope
Tests come in different shapes and sizes. To begin with, we need
to distinguish between the code paths a test is actually testing (aka
system under test or SUT) from the ones that are being run. The
SUT represents the scope of the test. It determines whether the test
is categorized as a unit test, an integration test, or an end-to-end
test.

A *unit* test validates the behavior of a small part of the codebase,
like an individual class. A good unit test should be relatively
static in time and change only when the behavior of the SUT
changes — refactoring, bug fixes, or new features shouldn’t break
it. To achieve that, a unit test should:
* use only the public interfaces of the SUT;
* test for state changes in the SUT (not predetermined
sequences of actions);
* test for behaviors, i.e., how the SUT handles a given input
when it’s in a specific state.

An *integration* test has a larger scope than a unit test, since it verifies
that a service can interact with an external dependency as expected.
Confusingly, integration testing has different meanings for different people. Martin Fowler makes the distinction between narrow
and broad integration tests. A *narrow* integration test exercises
only the code paths of a service that communicate with a specific
external dependency, like an adapter and its supporting classes. In
contrast, a *broad* integration test exercises code paths across multiple live services. In the rest of the chapter, we will refer to these
broader integration tests as end-to-end tests.

An *end-to-end* test validates behavior that spans multiple services
in the system, like a user-facing scenario. These tests usually run
in shared environments, like staging or production, and therefore
should not impact other tests or users sharing the same environment. Because of their scope, they are slow and more prone to
intermittent failures.

End-to-end tests can also be painful and expensive to maintain.
For example, when an end-to-end test fails, it’s generally not obvious which service caused the failure, and a deeper investigation
is required. But these tests are a necessary evil to ensure that user-facing scenarios work as expected across the entire application.
They can uncover issues that tests with smaller scope can’t, like
unanticipated side effects and emergent behaviors.

One way to minimize the number of end-to-end tests is to frame
them as user journey tests. A *user journey test* simulates a multi-step interaction of a user with the system (e.g., for an e-commerce
service: create an order, modify it, and finally cancel it). Such a
test usually requires less time to run than the individual journey
parts split into separate end-to-end tests.

As the scope of a test increases, it becomes more brittle, slow, and
costly. Intermittently failing tests are nearly as bad as no tests at
all, as developers stop trusting them and eventually ignore their
failures. When possible, it’s preferable to have tests with smaller
scope as they tend to be more reliable, faster, and cheaper. A good
trade-off is to have a large number of unit tests, a smaller fraction
of integration tests, and even fewer end-to-end tests.

## Size
The size of a test reflects how much computing resources it needs
to run, like the number of nodes. Generally, that depends on
how realistic the environment is where the test runs. Although the scope and size of a test tend to be correlated, they are distinct
concepts, and it helps to separate them.

A *small test* runs in a single process and doesn’t perform any blocking calls or I/O. As a result, it’s very fast, deterministic, and has a
very small probability of failing intermittently.

An *intermediate test* runs on a single node and performs local I/O,
like reads from disk or network calls to localhost. This introduces
more room for delays and non-determinism, increasing the likeli-
hood of intermittent failures.

A *large test* requires multiple nodes to run, introducing even more
non-determinism and longer delays.

Unsurprisingly, the larger a test is, the longer it takes to run and
the flakier it becomes. This is why we should write the smallest
possible test for a given behavior. We can use a *test double* in place
of a real dependency, such as a fake, a stub, or a mock, to reduce the
test’s size, making it faster and less prone to intermittent failures:
* A fake is a lightweight implementation of an interface that
behaves similarly to a real one. For example, an in-memory
version of a database is a fake.
* A stub is a function that always returns the same value no
matter which arguments are passed to it.
* Finally, a mock has expectations on how it should be called,
and it’s used to test the interactions between objects.

The problem with test doubles is that they don’t resemble how the
real implementation behaves with all its nuances. The weaker the
resemblance is, the less confidence we should have that the test
using the double is actually useful. Therefore, when the real implementation is fast, deterministic, and has few dependencies, we
should use that rather than a double. When using the real implementation is not an option, we can use a fake maintained by the
same developers of the dependency if one is available. Stubbing,
or mocking, are last-resort options as they offer the least resemblance to the actual implementation, which makes tests that use
them brittle.

For integration tests, a good compromise is to combine mocking
with contract tests. A *contract test* defines a request for an external
dependency with the corresponding expected response. Then the
test uses this contract to mock the dependency. For example, a con-
tract for a REST API consists of an HTTP request and response. To
ensure that the contract is valid and doesn’t break in the future, the
test suite of the external dependency uses the same contract definition to simulate the client request and ensure that the expected
response is returned.

## Practical considerations
As with everything else, testing requires making trade-offs. Suppose we want to end-to-end test the behavior of a specific API endpoint exposed by a service. The service talks to:
* a data store,
* an internal service owned by another team,
* and a third-party API used for billing
As suggested earlier, we should try to write the smallest possible test for the desired scope while minimizing the use of test doubles
that don’t resemble how the real implementation behaves.

Let’s assume the specific endpoint under test doesn’t communicate with the internal service, so we can safely use a mock in its
place. And if the data store comes with an in-memory implementation (a fake), we can use that in the test to avoid issuing network
calls. Finally, we can’t easily call the third-party billing API since
that would require issuing real transactions. However, assuming
a fake is not available, the billing service might still offer a testing
endpoint that issues fake transactions.

Here is a more nuanced example in which it’s a lot riskier to go
for a smaller test. Suppose we need to test whether purging the
data belonging to a specific user across the entire application stack
works as expected. In Europe, this functionality is mandated by
law (GDPR), and failing to comply with it can result in fines up to
20 million euros or 4% annual turnover, whichever is greater. In
this case, because the risk of the functionality silently breaking is
high, we want to be as confident as possible that it’s working as expected. This warrants the use of an end-to-end test that runs
in production periodically and uses live services rather than test
doubles.

## Formal verification
Software tests are not the only way to catch bugs early. Taking the
time to write a high-level description of how a system behaves, i.e.,
a *specification*, allows subtle bugs and architecture shortcomings to
be detected before writing a single line of code.

A specification can range from an informal one-pager to a formal
mathematical description that a computer can check. Since it’s
hard to specify what we don’t fully understand, a specification
can help us reason about the behaviors of the system we are designing. It also acts as documentation for others and as a guide
for the actual implementation. On top of the benefits mentioned
so far, by writing the specification in a formal language, we also
gain the ability to verify algorithmically whether the specification
is flawed (*model checking*).

Writing a specification doesn’t mean describing every corner of a
system in detail. The specification’s goal is to catch errors while
they are still cheap to fix. Therefore, we only want to specify those
parts that are most likely to contain errors and are hard to detect by
other means, like traditional tests. Once we have decided what to
specify, we also need to choose the level of abstraction, i.e., which
details to omit.

TLA+ is a well-known and widely used formal specification language. The likes of Amazon or Microsoft use it to describe some
of their most complex distributed systems, like S3 or Cosmos DB.

In TLA+, a *behavior* of a system is represented by a sequence of
states, where a state is an assignment of values to global variables.
Thus, the specification of a system is the set of all possible behaviors.

One of the goals of writing a specification is to verify that it satisfies properties we want the system to have, like safety and liveness. A *safety* property asserts that something is true for all states
of a behavior (invariant). A *liveness* property instead asserts that
something eventually happens. TLA+ allows to describe and verify properties that should be satisfied by all possible states and behaviors of a specification. This is extremely powerful, since a system running at scale will eventually run into all possible states and
behaviors, and humans are bad at imagining behaviors in which
several rare events occur simultaneously.

For example, suppose we have a service that uses key-value store
X, and we would like to migrate it to use key-value store Y that
costs less and has proven to perform better in benchmarks. At a
high level, one way we could implement this migration without
any downtime is the following:
1. The service writes to both data stores X and Y (dual write)
while reading exclusively from X.
2. A one-off batch process backfills Y with data from X created
before the service started writing to Y.
3. The application switches to read and write exclusively from
and to Y.

This approach might seem reasonable, but will it guarantee that
the data stores eventually end up in the same state?

If we were to model this with TLA+, the model checker would
be able to identify several problems, like a liveness violation that
leaves the system in an inconsistent state when a service instance
crashes after writing to A but before writing to B. The beauty of
automated model checking is that it returns an error trace with the
behavior (i.e., sequence of states) that violates the properties when
it fails.

Although modeling writes as atomic (i.e., either both writes succeed, or they both fail) fixes the liveness issue, the model isn’t correct yet. For example, if two service instances are writing to A and
B simultaneously, the two data stores can end up in different states
because the order of writes can differ.

You know we can solve this problem by introducing a message
channel between the service and data stores that serializes all
writes and guarantees a single global order. Regardless of the
actual solution, the point is that a formal model enables us to test
architectural decisions that would be hard to verify otherwise.
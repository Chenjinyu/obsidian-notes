Date: 2026-02-08
Course: [Saga Pattern for Orchestrate Distributed Transactions using AWS Step functions](https://medium.com/aws-lambda-serverless-developer-guide-with-hands/saga-pattern-for-orchestrate-distributed-transactions-using-aws-step-functions-2513db0de84e)
Tags: 

# Content

## One-line difference
- **Orchestration:** _commands_ driven by a central brain.
- **Choreography:** _events_ and local reactions, no central brain.
![](assets/1%20-%20Reliability%20-%20Sagas%20-%20Orchestration%20vs%20Choreography/file-20260208222547987.png)
## 1. Saga Orchestration (Orchestrator) (乐队指挥)
A **saga orchestrator** is a **central controller service** that **explicitly tells each participant service what to do next** in a multi-step transaction (the “saga”), and **decides when to run compensating actions** (rollbacks) if a step fails.
- **Control flow:** centralized (“do Step A → then Step B → then Step C”)
- **Coordination:** one service holds the saga state and drives transitions
- **Failure handling:** orchestrator triggers compensations in a defined order

a real example system architecture design
![](assets/1%20-%20Reliability%20-%20Sagas%20-%20Orchestration%20vs%20Choreography/file-20260208223310272.png)
## 2. Choreography(编舞, 一起的舞者)
Saga **choreography** is a **decentralized approach** where **no single service directs the whole workflow**. Instead, each service **reacts to events** (e.g., “OrderCreated”, “PaymentSucceeded”) and emits new events that trigger the next step.
- **Control flow:** distributed (“when you see event X, do Y, then emit Z”)
- **Coordination:** emerges from event interactions between services
- **Failure handling:** services emit compensating events when needed

In Choreography, there is no center orchestrator instead of events
![](assets/1%20-%20Reliability%20-%20Sagas%20-%20Orchestration%20vs%20Choreography/file-20260208221323831.png)

Using Kafka as the message brokers
![](assets/1%20-%20Reliability%20-%20Sagas%20-%20Orchestration%20vs%20Choreography/file-20260208221642880.png)

Saga Choreography handles the failures, below is PaymentFailed example
![](assets/1%20-%20Reliability%20-%20Sagas%20-%20Orchestration%20vs%20Choreography/file-20260208221740490.png)
# Note


# Reference


Date: 2025-10-26
Course:
Tags: [[Base Knowledge]] [[DevOps]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content
You got it. Here’s a single, no-fluff playbook that ties **all four deployment strategies** together and answers the concerns you raised: *what each one is, how traffic moves, who/what monitors what, how to implement (esp. in SageMaker), how to automate/roll back, and when to choose which.*

---
# Canary deployment

**What it is**
Roll out the **new version** to a **small % of real traffic** (e.g., 5%), watch live metrics, then ramp to 20% → 50% → 100% if healthy.

**Why we monitor**
Because real users see the canary. You monitor **user-visible metrics**: error rate (4xx/5xx), latency (p50/p95/p99), and **business KPIs** (e.g., conversion, model accuracy proxy if you compute it online).

**Who/what advances the rollout**
Usually **manual** (an engineer decides to ramp). Can be scripted/automated (guardrails) but philosophy is human-in-the-loop.

**SageMaker “how-to”**

* One endpoint with **two ProductionVariants** (old/new).
* Start with `InitialVariantWeight` like 0.95 old / 0.05 new.
* Shift weights with `UpdateEndpointWeightsAndCapacities`.

*Minimal Python ramp + rollback (you can adapt these):*

```python
# SageMaker - ramp
sm.update_endpoint_weights_and_capacities(
  EndpointName=endpoint,
  DesiredWeightsAndCapacities=[
    {"VariantName":"OldModel","DesiredWeight":0.8},
    {"VariantName":"NewModel","DesiredWeight":0.2},
])

# rollback (100% back to old)
sm.update_endpoint_weights_and_capacities(
  EndpointName=endpoint,
  DesiredWeightsAndCapacities=[
    {"VariantName":"OldModel","DesiredWeight":1.0},
    {"VariantName":"NewModel","DesiredWeight":0.0},
])
```

**What scripts you should have**

* **Smoke test** (sanity request to the endpoint).
* **Weight shifter** (ramp in steps).
* **Health checker** (queries CloudWatch for 5xx, latency, custom KPIs).
* **Rollback** (one command to 100% old).

**Pros / Cons**

* Safest way to expose new code/model to production.
  − Slower, needs discipline + tooling.

**Use when**
You want **low risk** and need to see **real-user impact** before going all-in.

---

# A/B testing

**What it is**
Run **two (or more) versions in parallel** with a fixed split (e.g., 50/50). Goal is **comparison**, not rollout.

**Why we monitor**
To decide the **winner**. You compare **experiment metrics** across variants (accuracy/F1, engagement, revenue, etc.). It’s not about safety; it’s about **which is better**.

**Who/what advances the rollout**
Humans (PM/DS/engineer) decide after the experiment window. You may later promote the winner to 100%.

**SageMaker “how-to”**

* Same as canary (multiple **ProductionVariants**), but the split is **deliberately fixed** for the test window, and you analyze results offline/near-real-time.
* When a winner is chosen, change weights to 100/0 or update the endpoint config.

**Pros / Cons**

* Gives statistical evidence.
  − Costs more (two versions live), not meant to finish with 100% new automatically.

**Use when**
You need **evidence** that B beats A (models, features, pricing, etc.).

---

# Blue/Green deployment

**What it is**
Maintain **two complete environments**: **Blue** (current) and **Green** (new). Flip **all traffic** at once from Blue → Green. Flip back if needed.

**Why we monitor**
You’ll still watch errors/latency/KPIs, but the *critical check* is just before/after the **cutover** since the switch is atomic.

**Who/what advances the rollout**
Human decision (press the switch), often with a short bake phase on Green behind shadow or pre-prod tests.

**SageMaker “how-to”** (two common patterns)

* **Two endpoints** (e.g., `endpoint-blue`, `endpoint-green`). Use a router (API Gateway/ALB) or a config flag to flip traffic.
* Or **one endpoint** and swap **EndpointConfig** (Green model/config) in a single update; roll back by swapping back.

**Pros / Cons**

* **Instant rollback**, minimal downtime.
  − Requires **duplicate capacity** (higher cost during release).

**Use when**
You need **near-zero downtime** and **fast rollback** (e.g., critical APIs).

---

# Rolling deployment

**What it is**
Gradually **replace instances/pods** of the old version with the new version in **batches** until everything runs the new version (e.g., 2 of 10 at a time).

**Why we monitor**
The **platform** (Kubernetes/ECS/SageMaker hosting) uses **health checks/readiness** to decide if each batch is healthy. Focus is **infrastructure stability** (pods up, passing probes), not experiment KPIs.

**Who/what advances the rollout**
**Automatic** once triggered—the orchestrator keeps replacing batches if health checks pass. If a batch fails, it halts/rolls back that batch.

**SageMaker “how-to”**

* Update the **EndpointConfig** to the new model/artifacts.
* SageMaker hosting performs a **rolling replacement** of instances behind the endpoint.
* You can tune **rolling behavior** with instance counts and autoscaling, but conceptually it’s automatic.

**Pros / Cons**

* No need for duplicate full env; smooth upgrade.
  − **Rollback is heavier** (you re-deploy the old version to instances that were already upgraded).

**Use when**
You want a **cost-efficient**, low-downtime upgrade and don’t need controlled experiment traffic.

---

## Why the monitoring differs

* **Canary:** real users see a slice → watch **user-visible metrics** + **business KPIs** to decide whether to ramp.
* **A/B:** it’s an **experiment** → compare **metrics across variants** to pick a winner.
* **Rolling:** it’s **infra replacement** → the **platform** checks **health probes** (readiness/liveness, 200 OK) to continue.

---

## SageMaker quick-map (what to use where)

| Goal                      | SageMaker primitive                                                                | Notes                                                           |
| ------------------------- | ---------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Canary (risk-controlled)  | **Multiple ProductionVariants** in one endpoint + **update weights**               | Start 95/5 → ramp. Use CloudWatch alarms + scripted guardrails. |
| A/B test (compare)        | **Multiple ProductionVariants** at fixed split                                     | Capture data, compute metrics, then promote the winner.         |
| Blue/Green (instant flip) | **Two endpoints** (Blue/Green) and switch at router **or** swap **EndpointConfig** | Easiest rollback story; higher temporary cost.                  |
| Rolling (auto replace)    | **UpdateEndpoint** to new config; hosting rolls instances                          | Orchestrated by SageMaker hosting; health checks gate progress. |

---

## Guardrails & scripts you’ll actually want (SageMaker)

* **Smoke test**: send a known payload and validate schema/latency.
* **Data capture** (optional): enable on the endpoint to compare responses offline.
* **Health checks / alarms**: CloudWatch alarms for 5xx rate, p95 latency, TPS drops, and custom KPIs (if you emit them).
* **Weight shifter** (for canary/A-B): scripted steps with pauses + health assertions.
* **Rollback**: one command to set weights back to 100% old (canary/A-B) or swap configs (Blue/Green) or re-deploy old (Rolling).
* **Runbook**: short README with commands, metrics to watch, and “stop the bleeding” steps.

---

## Choose quickly (decision cheats)

* **Minimize risk with real traffic?** → **Canary**.
* **Prove which version is better?** → **A/B**.
* **Zero-downtime + instant rollback?** → **Blue/Green**.
* **Cost-efficient gradual upgrade, autopilot once started?** → **Rolling**.



# Note


# Reference


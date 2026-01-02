Date: 2025-10-26
Course:
Tags: 
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content
Great question 👍 — Apache **Flink** and Apache **Kafka** are often mentioned together, but they solve **different problems** in the data streaming ecosystem. Here’s the breakdown:

---

## 🔹 Apache Kafka

* **What it is**: A **distributed event streaming platform** (messaging system + storage + streaming).
* **Core role**: Acts as a **log-based message broker** — stores and transports streams of records (events) between producers and consumers.
* **Key features**:

  * Durable event storage (retains events for configurable time).
  * High throughput, scalable pub/sub messaging.
  * Good for decoupling producers and consumers.
  * Handles replaying messages (consumers can re-read).
* **Use cases**:

  * Event bus for microservices.
  * Collecting logs/metrics and streaming them to systems.
  * Real-time ETL pipelines (with Kafka Connect).
  * Buffer between producers and downstream consumers.

---

## 🔹 Apache Flink

* **What it is**: A **stream processing framework**.
* **Core role**: Processes data in **real-time (streaming)** or **batch mode**, with strong state management and low latency.
* **Key features**:

  * Stateful stream processing (can keep track of running aggregates, sessions, windows, etc.).
  * Event-time and out-of-order event handling.
  * Exactly-once state consistency guarantees.
  * Supports SQL queries on streams.
* **Use cases**:

  * Real-time analytics dashboards.
  * Fraud detection, anomaly detection.
  * Complex event processing (CEP).
  * Continuous ETL and enrichment.

---

## 🔄 How They Work Together

* Kafka is often the **data pipeline backbone**, where events are produced and stored.
* Flink consumes events from Kafka, applies transformations, aggregations, or machine learning models, and outputs to databases, data lakes, or other systems.

👉 Example:

* **Kafka** collects clickstream data from millions of users.
* **Flink** processes the streams in real time to compute user behavior metrics (like session time, top pages, fraud detection).

---

✅ **In short**:
* **Kafka = data transport & storage (event streaming backbone)**
* **Flink = data processing (stream/batch computations)**



# Note


# Reference
[[Amazon MSK Lambda]]

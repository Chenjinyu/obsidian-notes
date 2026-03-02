PACELC is an extension of CAP theorem proposed by Daniel Abadi in 2012. It addresses the biggest criticism of CAP — that CAP only describes what happens during a network partition, but says nothing about the trade-offs that exist in normal operation.
The name breaks down into two scenarios:

if Partition (P):
    trade-off between Availability (A) vs Consistency (C)
Else (E) — normal operation:
    trade-off between Latency (L) vs Consistency (C)


So written out: PAC + ELC → PACELC

The Two Scenarios Explained
PAC side — during a Partition:
This is just CAP. When a network partition happens, you must choose between staying Available (respond even with possibly stale data) or staying Consistent (refuse to respond until the partition heals).
ELC side — during normal operation (no partition):
Even when everything is working fine, there is still a fundamental trade-off between Latency and Consistency. This is the key insight Abadi added.
To achieve strong consistency in a distributed system, a write operation must be replicated and acknowledged by multiple nodes before returning success. That synchronization takes time, which increases latency. If you want low latency, you write to one node and replicate asynchronously — but then reads on other nodes may return stale data, meaning weaker consistency.

How Real Systems Are Classified
Systems are typically described with two letters for each side, like PA/EL or PC/EC:



|System          |Partition behavior     |Normal operation      |Notes                                 |
|----------------|-----------------------|----------------------|--------------------------------------|
|Cassandra       |PA (favor Availability)|EL (favor Latency)    |Highly available, eventual consistency|
|DynamoDB        |PA                     |EL                    |Similar to Cassandra                  |
|MongoDB         |PC (favor Consistency) |EC (favor Consistency)|Can be tuned                          |
|Zookeeper       |PC                     |EC                    |Strong consistency                    |
|MySQL/PostgreSQL|PC                     |EC                    |Traditional RDBMS                     |
|CRDT systems    |PA                     |EL                    |Conflict-free replicated types        |

Why PACELC is More Useful Than CAP
CAP has a practical problem — as mentioned before, partition tolerance is non-negotiable in distributed systems, so CAP really only tells you “CP or AP?” and nothing else. PACELC gives you a richer picture:
CAP asks: What happens when things go wrong?
PACELC asks: What happens when things go wrong and what are you trading off every single day in normal operation?
For most real systems, the ELC trade-off is actually more relevant day-to-day than the PAC trade-off, because partitions are rare events but latency vs consistency is a constant engineering decision affecting every read and write.

Simple Analogy
Think of a bank with multiple branches sharing a central ledger:
	∙	During a network outage (PAC): Do you let branches keep processing transactions (Available) or freeze everything until connectivity is restored (Consistent)?
	∙	During normal operation (ELC): Do you require every transaction to be confirmed by the central ledger before completing (Consistent but slow), or do you let branches operate locally and sync later (Fast but possibly inconsistent)?
PACELC captures both questions, making it a much more complete framework for reasoning about distributed database design.​​​​​​​​​​​​​​​​
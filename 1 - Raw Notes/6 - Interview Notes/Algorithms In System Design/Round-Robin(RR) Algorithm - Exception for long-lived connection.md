Date: 2026-02-16
Course:
Tags: [[Round Robin]] [[Round-Robin(RR) Algorithm]][[../../7 - JCUS.LINK/System Design]] [[Algorithms]] [[System Design Interview]]

# Content

**_Round Robin (RR)_** _is a CPU scheduling algorithm that gives_ **_each process a fixed amount of time_** _(called a_ **_time quantum_**_) to execute. If the process doesn’t finish in that time, it goes to the back of the queue, and the next process gets its turn._

## Key Terminologies
- **Process:** A task or program waiting to be executed.
- **Time Quantum / Time Slice:** A small fixed amount of CPU time given to each process.
- **Ready Queue:** A line (queue) where processes wait for their turn to run.

##  How Round Robin Works
1. All processes are placed in a queue.
2. The first process gets the CPU for a time quantum.
3. If the process finishes in that time, it leaves the queue.
4. If not, it goes to the back of the queue to wait for another turn.
5. This continues in a circular manner until all processes are completed.


![](assets/Round-Robin(RR)%20Algorithm%20-%20Exception%20for%20long-lived%20connection/file-20261118234722379.png)
The BT(Burst time) is the amount of CPU execution time for a process needed. 中文叫「CPU 執行時間」。
TQ = Time Quantum, which is the amount of CPU execution time in each turn

## Example of Round Robin Scheduling

Let us consider a system that has four processes which have arrived at the same time in the order P1, P2, P3 and P4. The burst time in milliseconds of each process is given by the following table −

|Process|CPU Burst Times in ms|
|---|---|
|P1|8|
|P2|10|
|P3|6|
|P4|4|

Let us consider time quantum of 2ms and perform RR scheduling on this. We will draw GANTT chart and find the average turnaround time and average waiting time.

### GANTT Chart with time quantum of 2ms

![GANTT Chart with time quantum of 2ms](https://www.tutorialspoint.com/operating_system/images/gantt_chart_with_time_quantum_of_2ms.jpg)

### Average Turnaround Time

Average TAT = Sum of Turnaround Time of each Process **/** Number of Processes
=(TATP1+TATP2+TATP3+TATP4)/4
= ( 24 + 28 + 22+ 16) / 4 = 22.5 ms

In order to calculate the waiting time of each process, we multiply the time quantum with the number of time slices the process was waiting in the ready queue.

### Average Waiting Time
Average WT = Sum of Waiting Time of Each Process **/** Number of processes
=(WTP1+WTP2+WTP3+WTP4)/4
= ( 8*2 + 9*2+ 8*2+ 6*2) / 4 = 15.5 ms



---

**Round Robin does NOT replace existing connections and it does NOT cause an error.**  
It simply keeps assigning **new connections** in order, **ignoring how long old ones stay open**.

Long-lived connections just… stay open.

---
### What actually happens step by step
Assume 3 servers: A, B, C  
Round Robin sequence: A → B → C → A → B → C …
Now imagine:
- Connections to **A** are long-lived (WebSockets, streaming)
- Connections to **B** and **C** are short-lived
#### Timeline
1. Client 1 → A (long connection, stays open)
2. Client 2 → B (short, closes quickly)
3. Client 3 → C (short, closes quickly)
4. Client 4 → A (**another** long connection)
5. Client 5 → B
6. Client 6 → C

Result after a while:
- Server **A** has many active connections
- Servers **B** and **C** are mostly idle

Round Robin **does not care**. It never checks connection count or load.

---
### Key points to be very clear about
- ❌ **No connection replacement**
- ❌ **No forced closing**
- ❌ **No error by default**
- ✅ Existing connections stay until the client or server closes them
- ✅ Only **new connections** are scheduled

If a server becomes overloaded:
- The load balancer **keeps sending traffic anyway**
- Eventually the server itself may:
    - Respond slowly
    - Time out
    - Reject connections
    - Crash (worst case)

That failure is **not caused by Round Robin directly**, but by its lack of awareness.

---
### Why this is a problem
Round Robin assumes:
> All connections cost roughly the same
When that assumption is false (long-lived connections):
- Load becomes uneven
- One server can get overwhelmed
- Latency increases

This is why Round Robin is **bad for**:
- WebSockets
- Streaming
- gRPC streams
- File uploads
- Chat systems

---

### What systems do instead
For long-lived or uneven(不均匀) connections, use:
- **Least Connections**
- **Weighted Least Connections**
- **Least Response Time**
- **Connection-aware load balancing**

These **avoid sending new traffic to already busy servers**.

---
### Mental model (remember this)
> **Round Robin is blind.**  
> It hands out tickets in order and never looks back.

# Note


# Reference


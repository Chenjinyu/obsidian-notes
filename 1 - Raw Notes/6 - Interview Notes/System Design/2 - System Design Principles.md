Date: 2026-01-27
Course:
Tags: 

# Content

## Purpose of System Design
How do we architect a system that supports the functionality and requirements of a system in the _**best way**_ possible? The system can be "best" across several different dimensions in system-level design. These dimensions include:

- **Scalability:** a system is scalable if it is designed so that it can handle additional load and will still operate efficiently.
- **Reliability:** a system is reliable if it can perform the function as expected, it can tolerate user mistakes, is good enough for the required use case, and it also prevents unauthorized access or abuse.
- **Availability:** a system is available if it is able to perform its functionality (uptime/total time)**.** Note reliability and availability are related but not the same. Reliability implies availability but availability does not imply reliability.
- **Efficiency:** a system is efficient if it is able to perform its functionality quickly. Latency, response time and bandwidth are all relevant metrics to measuring system efficiency.
- **Maintainability:** a system is maintainable if it easy to make operate smoothly, simple for new engineers to understand, and easy to modify for unanticipated use cases.
## Simple Distributed System Example:

Let us consider a simple write system. The web service is designed to allow users to write and save information, and get an associated URL with the associated text that they have written (like PasteBin).
![](assets/2%20-%20System%20Design%20Principles/file-20260127222753562.png)

- **Scalable.** The use of load-balancers and caches and the choice of databases (object storage S3 and noSQL) will help facilitate additional load on the system from additional users.
- **Reliable.** The system will be able to reliably handle the functionality (i.e. where some number of clients are able to write text and get an associated URL with the text they have written) and by how the APIs are defined (not shown), should be able to handle user mistakes.
- **Efficient.** The introduction of the caching allows for greater efficiency for read requests by the user. The load-balancing also distributes the load more evenly across servers to make the system more efficient.
- **Available.** The load-balancers are distributing the load across multiple servers, meaning there is less likelihood of failure that will cause the system to crash. Additional databases can be used for redundancy in the case of error or failures.
- **Maintainability.** The APIs (not pictured here) are designed in a way that allows for modularity (i.e. separation of read and write calls). This allows for easy maintainability of the system.

You should _**always**_ have the above distributed system properties (scalability, reliability, efficiency, availability and maintainability) in the back of your mind as you walk through each of the steps in the system-design interviews!

## System Design Toolbox
There are so many components, algorithms, and architectures that support optimality in the above dimensions of distributed system design.
![](assets/2%20-%20System%20Design%20Principles/file-20260127222830941.png)

You will quickly find that each element in the system design toolbox may be **great with respect to one dimension but at the cost** of being low-performing in another (i.e. a component might be extremely efficient but not as reliable, or a certain design choice might be really effective at supporting one functionality like providing read access but not as efficient with write access).
![](assets/2%20-%20System%20Design%20Principles/file-20260127222843159.png)
In other words, there are **tradeoffs** that you must consider as you make informed system design choices. The best way to understand these tradeoffs is to understand how each of these components, algorithms and architectural designs work. In particular it is helpful to know how each element (tool):

- Works independently.
- Compares to other tools that perform similarly.
- Fits together in the bigger picture of system-level design.
# Note


# Reference


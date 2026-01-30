Date: 2026-01-10
Course:
Tags: 

# Content

Here is your content **cleaned up and written in clear, correct English**, keeping the same structure and examples.
---
## SOLID Principles
### 1. **S — Single Responsibility Principle (SRP)**
A class should have **only one reason to change**, meaning it should be responsible for **only one thing**.
**Example:**
A `User` class should not:
* handle user data,
* send emails, **and**
* manage database connections.
These responsibilities should be separated into different classes so that each class focuses on a single concern.
---
### 2. **O — Open/Closed Principle (OCP)**
Software entities (classes, modules, functions) should be **open for extension but closed for modification**.
This means new functionality should be added by **extending existing code**, not by modifying it.
---
### 3. **L — Liskov Substitution Principle (LSP)**
Subclasses should be **substitutable for their base classes** without affecting the correctness of the program.
**Example:**
If a `Bird` class has a `fly()` method, then letting `Penguin` inherit from `Bird` violates LSP, because penguins cannot fly. Using such a subclass would break expected behavior.
---
### 4. **I — Interface Segregation Principle (ISP)**
Clients should **not be forced to depend on interfaces they do not use**.
Instead of one large, bloated interface, create **multiple smaller, specific interfaces**.

**Example:**
Instead of a single `IAnimal` interface with many methods, split it into smaller interfaces such as:
* `IFlyable`
* `ISwimmable`
This way, classes only implement the interfaces they actually need.
---
### 5. **D — Dependency Inversion Principle (DIP)**
High-level modules should **not depend on low-level modules**.
Both should depend on **abstractions**.
Additionally:
* Abstractions should not depend on details.
* Details should depend on abstractions.
**Example:**
Business logic should not depend directly on a concrete database class.
Instead, it should depend on a data access interface, so that changing the database implementation does not require changes to the business logic.

Summary (one sentence)

> SOLID principles help you design software that is **flexible, maintainable, and scalable** by enforcing good object-oriented design practices.


OOD (Object-Oritened Design)
Four Pillars:
1. Encapsulation
2. Inheritance
3. Polymorphsim
4. Abstraction.

for Database:
1. Aduit/history tracking for System of Records(SOR) - is the authoritative data source:  so that we can know when, what and who. 
for example: 
users and users_hisotry(id, status, valid_from, valid_to, updated_by) tables:
- when a user update, then copy the old data to user_history, and then update users table. (Create trigger for UserHistory funcion before insert/update table `users`.)

2. create a function on a scheudle to delete old data by monthly, 3 months, etc(needs pg_cron extension, orcale has build-in: DBMS_SCHEDULER).

3. use views for data combination from different tables. (Specific for bank usecase, views for NPI) 

4. setup versioning control for source of truth(SoT). (it might store each changes of versons, and query can alwasys get the latest one, but this design) <- this is thinking about the evidence table, when end users upload excel to gather the evidece, how can we capture and track the history. (need double check the tables, and understand more.)

SOR - The authoritative current state
System of Record (SoR) - The immutable history of facts

---------
A System of Record (SOR) is the authoritative application for a specific data domain (like a CRM for customer info), while a Source of Truth (SOT), often a data warehouse or data lake, is the unified, trusted view compiled from multiple SORs, offering a complete, clean picture for decision-making, ensuring data consistency across the organization. An SOR is about where data originates and lives for one purpose, whereas a SOT is about which version of data is most reliable for broad organizational use. [1, 2, 3]  
System of Record (SOR) 

• Definition: The primary, authoritative system where specific business data is created, updated, and maintained (e.g., your accounting software for financial records, HR system for employee data). 
• Focus: Operational data capture and management within its specific domain. 
• Example: Your CRM is the SOR for customer contact details. [1, 2, 3, 4]  

Source of Truth (SOT) 

• Definition: A consolidated, harmonized view of data from various SORs, cleansed and validated to be the most accurate, consistent, and reliable data asset. 
• Focus: Data governance, integration, and providing a single, trusted dataset for analytics and decisions. 
• Example: A data warehouse pulling customer data from CRM, billing, and support systems to create one master customer profile. [1, 2, 3, 5, 6]  

Key Differences 

• Scope: SOR is domain-specific; SOT is enterprise-wide and holistic. 
• Function: SOR captures data; SOT unifies and trusts data. 
• Relationship: An SOT often pulls data from multiple SORs, acting as a bridge between them. 
• Example Scenario: Your sales system (SOR) says a customer is in "CA," but your billing system (SOR) says "California." The SOT integrates these, resolves the conflict (perhaps based on a defined rule), and presents one consistent "California" for all reports. [1, 2, 3, 7, 8]  


[1] https://business.adobe.com/blog/basics/systems-of-record
[2] https://www.ibm.com/think/topics/system-of-record-vs-source-of-truth
[3] https://blog.logrocket.com/product-management/what-is-a-single-source-of-truth/
[4] https://www.linkedin.com/pulse/difference-between-system-record-source-truth-santosh-kudva
[5] https://nulab.com/learn/project-management/single-source-of-truth-what-is-it-and-why-do-you-need-it/
[6] https://www.getreba.com/blog/bi-single-source-of-truth
[7] https://www.gaine.com/articles/system-of-record-vs-system-of-reference-why-you-need-both-for-reliable-healthcare-data
[8] https://www.quora.com/What-is-the-difference-Between-System-of-Record-and-Source-of-Truth



# Note


# Reference


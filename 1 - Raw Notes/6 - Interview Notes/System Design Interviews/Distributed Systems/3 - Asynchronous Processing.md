Date: 2026-02-16
Course:
Tags: [[System Design]] [[Asynchronous]] [[Distributed System]]
 
# Content

# Asynchronous Processing

### In this lesson, we explain what you need to know about asynchronous processing for system design interviews.

The difference between synchronous and asynchronous processing can trip candidates up if they're not careful, so let's review.

## Synchronous vs. asynchronous processes[](https://www.tryexponent.com/courses/system-design-interviews/asynchronous-processing#synchronous-vs-asynchronous-processes)

**Synchronous processes** run one after the other, and each task must be 100% complete before the next operation begins. Imagine ordering a sub at Subway. Your sandwich artist puts together your sub based on your inputs in real-time, according to a set workflow. Bread, protein, toppings, then sauce. This is a synchronous process.

**Asynchronous (or async) processes** can work independently and in parallel. In other words, you don't have to wait for task A to be 100% complete before beginning task B. This is more akin to ordering takeout. You place a complete order including a meal, drink, and dessert, and you're told to pick it up in 20 minutes. You're now free to use that time as you like.

## Why async processing matters[](https://www.tryexponent.com/courses/system-design-interviews/asynchronous-processing#why-async-processing-matters)

Not all tasks can be performed synchronously without sacrificing user experience or system reliability. Google can't crawl the web in real-time with every search, and YouTube can't process all the videos being uploaded simultaneously. At some scale, a system will become unreliable because it won't be able to handle the load, or the task will just take too long.

Even when synchronous processing is technically feasible, async can be a huge cost and response-time saver, as long as tasks _can_ be run independently. For example, in most popular apps users upload, save, and share data. Many operations run in the background as changes are made to the database, but if the user is made to wait until every step is complete, the UX would be extremely negative.

## How it works[](https://www.tryexponent.com/courses/system-design-interviews/asynchronous-processing#how-it-works)

There are several different flavors of asynchronous processing to choose from. Some popular options include:

### Batch processing

Commonly used in applications where large amounts of data are processed regularly for periodic review. Corporate finance and accounting software would be well-suited to batch processing.

Perhaps the most popular implementation of this is **MapReduce,** a model for batch processing introduced by Google in 2004. It's a simple algorithm:
![](assets/3%20-%20Asynchronous%20Processing/file-20260216222407312.png)
_Image via [Big Data Analytics for Sensor-Network Collected Intelligence](https://www.sciencedirect.com/topics/engineering/mapreduce)_

The reduced input is automatically sorted and stored for easy access. In addition to applications where regular review is needed, batch processing strategies like MapReduce work well in situations where _running in parallel helps speed up the task._ For example, if you have a complex analytics task where running on one machine would take days or weeks, splitting it across many processes makes it faster. Google uses it to process and index many different web pages in parallel. Note that MapReduce won't work as well for data that's not repetitive, as it won't condense down (reduce) as much.

### **Stream processing**

With stream processing, data flows into your system as **events** occur. Events may be changes in state, or updates — for example, a customer clicking on an ad is an event. Stream processing will get you close-to-real time results which is valuable in applications where accuracy is critical such as a trading platform. These benefits are offset by complexity and fragility, however. **Check-pointing** can help alleviate problems with system outages, but you'll have to give careful consideration to checkpoint frequency. Frequent checkpoints mean faster recovery, but lower performance... which is the entire reason for going with stream processing in the first place.

### **Lambda architecture**

Lambda architecture can bridge the gap between durable-yet-delayed batch processing and fresh-yet-brittle stream processing by creating a "fast lane" for processing priority events, but this introduces operational complexity.

## **Asynchronous queues**[](https://www.tryexponent.com/courses/system-design-interviews/asynchronous-processing#asynchronous-queues)

Queues make asynchronous processes more reliable and less brittle as events are captured and processed in an orderly way. **Task queues** are a type of **message queue**; sometimes they're built on top of message queues. For example, Celery supports many different "**message brokers**", such as Redis, RabbitMQ, and Amazon SQS. Generally:

- **Message queues**, which receive, log, and deliver messages, can be used to update users that jobs are being processed in the background, thus unblocking them and making for a better user experience. Redis and RabbitMQ are both popular choices.
- **Task queues** execute in addition to passing information. They schedule jobs, complete tasks, and report results. Celery is a popular choice.

**Publish/Subscribe (or pub/sub)** messaging is another async communication method to know. In pub/sub messaging, you have a _subscriber_ who receives a message sent by a _publisher_ via a _broker_. Because communication is decoupled, messages can be automatically pushed to all subscribers rather than pulled individually via a message queue. This method is popular in event-driven architecture because event-driven services can be delivered quickly and easily. Additionally, because publishers are isolated from subscribers, the system is easier to maintain and secure.

![](assets/3%20-%20Asynchronous%20Processing/file-20260216222435683.png)
## When to bring it up in an interview[](https://www.tryexponent.com/courses/system-design-interviews/asynchronous-processing#when-to-bring-it-up-in-an-interview)

Consider async processing for applications with:

- Long expected processing times, or when the processing time is unclear.
- No need for immediate processing. A classic example is Facebook's newsfeed. A newly uploaded post will be immediately visible in your own feed but it may take some time before it's visible to your entire network.

Batch processing is useful when you need to process chunks of data in predictable intervals, as in accounting software. Stream processing is a good choice for applications like anomaly detection or sentiment analysis when timeliness is critical, and lambda architecture can help you capture the benefits of both if you're willing to deal with added complexity. Synchronous processing is still the best choice for simple applications where processing times are short and well-defined, and when errors must be dealt with immediately like in payment tools.

Take a look at the below table to help guide your decisions when prepping for your interview:
![](assets/3%20-%20Asynchronous%20Processing/file-20260216222449604.png)
# Note


# Reference


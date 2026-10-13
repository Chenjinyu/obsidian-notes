---
sr-due: <% tp.date.now("YYYY-MM-DD", 3) %>
sr-interval: 1
sr-ease: 2.5
---
### SSE connection here stands for Server-side Event. 
It lets a server keep an HTTP **response open** and continuously send updates to a client. BUT SSE itself is not **REST**, its a streaming mechanism that an HTTP API an use. 
SSE carries events from server to client, the client sends its requests separately through HTTP. 

A typical flow looks like this:

1. The client sends an HTTP request.
2. The server responds with `Content-Type: text/event-stream`.
3. The server keeps the response open and sends events as they become available.
4. The connection closes when the work finishes, the client disconnects, or a timeout occurs.

For example, the server could send these events several seconds apart:
```text
event: progress
data: {"percentage": 20}

event: progress
data: {"percentage": 70}

event: complete
data: {"result": "Report generated"}
```

**These are chunks of one ongoing HTTP response—not separate HTTP responses.** The client reads each event as it arrives.

|Regular HTTP API response|SSE response|
|---|---|
|Returns a complete response, then finishes|Sends events incrementally while remaining open|
|Client may poll for progress|Server pushes progress when available|
|Often `application/json`|`text/event-stream`|

### One FastAPI + browser example. 

---
sr-due: <% tp.date.now("YYYY-MM-DD", 3) %>
sr-interval: 1
sr-ease: 2.5
---
#review/7d 

## Takeaways
1. MPC is stateful session, should say `protocal session`, because the session across sessions and connections. 
2. Retain information depends on the design, not required one particular session JSON object.
3. 
### In session-based MCP, “stateful” primarily refers to the **protocol session between the MCP client and server**, rather than the user’s conversation.

**The session ID identifies the state; the ID alone isn’t what makes it stateful.** The server retains information associated with that session across requests, such as negotiated capabilities and session-specific application data. 
The exact storage structure depends on the SDK; MCP does not require one particular session JSON object.

```text
Client initializes → Server creates session ABC

Request 1 + session ABC → Server uses ABC’s existing state
Request 2 + session ABC → Server uses that same state
```

That session can span multiple HTTP requests and connections, so **“protocol session” is more precise than “connection session.”** The client includes `Mcp-Session-Id` on subsequent requests.

**Your chatbot’s conversation history remains separate.** The MCP server knows the conversation only if your application explicitly sends or exposes it.


#### **1. Information established during initialization**

Your Next.js backend’s MCP client sends an initialization request like this:

```
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-11-25",
    "clientInfo": {
      "name": "internal-nextjs-chatbot",
      "version": "1.0.0"
    },
    "capabilities": {
      "roots": {
        "listChanged": true
      },
      "elicitation": {
        "form": {}
      }
    }
  }
}
```

The capabilities above are examples; your client should advertise only features it implements. During initialization, the client and server exchange implementation details and capabilities and agree on a protocol version. [Model Context Protocol](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle?utm_source=chatgpt.com)

##### The server’s retained session information can **conceptually** look like:

```
{
  "sessionId": "mcp_session_abc123",
  "negotiatedProtocolVersion": "2025-11-25",
  "initialized": true,
  "clientInfo": {
    "name": "internal-nextjs-chatbot",
    "version": "1.0.0"
  },
  "clientCapabilities": {
    "roots": {
      "listChanged": true
    },
    "elicitation": {
      "form": {}
    }
  },
  "loggingLevel": "warning"
}
```

##### This is an illustrative representation, not an actual standardized storage schema.

|Field|Why the server retains it|
|---|---|
|`sessionId`|Associate subsequent HTTP requests with this session|
|`negotiatedProtocolVersion`|Know which protocol rules apply|
|`initialized`|Track whether initialization has completed|
|`clientInfo`|Know which client application and version connected|
|`clientCapabilities`|Know whether the client supports features such as elicitation|
|`loggingLevel`|Remember the level requested through `logging/setLevel`, if set|

For a concrete SDK example, the official C# SDK exposes `SessionId`, `NegotiatedProtocolVersion`, `ClientInfo`, `ClientCapabilities`, and `LoggingLevel`. The logging level is initially unset unless the client sets it. [MCP C# SDK](https://csharp.sdk.modelcontextprotocol.io/v1/api/ModelContextProtocol.Server.McpServer.html?utm_source=chatgpt.com)

**Notice: `clientInfo` identifies the application—not the logged-in employee.**

#### **2. Runtime information accumulated during the session**

##### Depending on enabled features and implementation, the server may also track:

|Runtime state|Example|Purpose|
|---|---|---|
|Pending requests|Request `42` is awaiting a response|Match a response to its outstanding request|
|Active operations|Tool request `57` is running|Handle progress and cancellation|
|Resource subscriptions|Client subscribed to `repo://acme/checkout/status`|Know which resource-change notifications to send|
|Stream routing|An active SSE stream associated with the session|Deliver messages to the correct client|
|Replay records, if configured|SSE event IDs and retained events|Resume delivery after a disconnect|
|Expiration bookkeeping|Last activity time / expiration deadline|Clean up inactive sessions|

These are **operational records**, not a transcript of completed tool calls or user messages. Streamable HTTP supports session association and optional event replay; replay storage is not automatically required for every server. [Model Context Protocol](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports?utm_source=chatgpt.com)

#### **3. Business data your team explicitly adds**

For your GitHub integration, your developers could additionally maintain:

```
{
  "sessionId": "mcp_session_abc123",
  "applicationState": {
    "selectedRepository": "acme/checkout",
    "activeDraftId": "draft_789",
    "lastCreatedIssueNumber": 317
  }
}
```

**MCP does not automatically create or populate these fields.** Your tool handlers must write and read them.

For example:

```
Call 1: select_repository("acme/checkout")
        Your code stores selectedRepository.

Call 2: create_issue(title, body)
        Your code reads selectedRepository.
```

Without that custom implementation, the second call would need the repository explicitly:

```
create_issue(repository, title, body)
```

For a durable draft, I would store `draft_789` in your business database and pass its ID explicitly. That lets the task continue even after the MCP session expires.

So, when you inspect an MCP session, expect **protocol settings and communication bookkeeping**. Repository selection, draft contents, user identity, and conversation history exist there **only if your application deliberately integrates them**.
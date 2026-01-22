Date: 2025-12-20
Course:
Tags: [[LLM]] [[AI Agent]] [[MCP

# Content
**MCP SDK Client (with initialization):**
- Expects a **persistent connection** (**stdio, WebSocket**, etc.)
- You initialize once → connection stays open → call tools through it
- Stateful — the server remembers the session
- Example: `mcpClient.connect(transport)` → `await mcpClient.initialize()` → then call tools

**Direct HTTP requests:**
- Each request is **stateless** — no persistent connection
- No initialization needed — just POST JSON-RPC and get response
- Each call is independent
- Example: `fetch(url, POST request)` → immediate response
**Your MCP server config:**
```python
mcp_app = mcp.http_app(
    path="/",
    transport="streamable-http",
    stateless_http=True,  # ← KEY: stateless
)
```

The `stateless_http=True` means **the server doesn't maintain sessions**. Each HTTP request is independent.

---

**If you want to use the SDK client approach**, you'd need your MCP server to support a persistent transport like:
```python
transport="stdio" # or "websocket"
```

Then the SDK client could initialize a persistent connection.
# Note


# Reference


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
## The SSE can be implemented by FastAPI and FastMCP

**the application logic is similar, but FastMCP handles the MCP protocol and streaming for you.** You define a tool and report progress instead of manually creating SSE events.

| FastAPI example                      | FastMCP example                                    |
| ------------------------------------ | -------------------------------------------------- |
| Define `GET /events`                 | Define a tool with `@mcp.tool()`                   |
| Manually format `event:` and `data:` | Call `ctx.report_progress()`                       |
| Client parses SSE text               | MCP client handles messages and invokes a callback |
| Define your own completion event     | Return the tool’s result                           |

### One FastAPI + browser example via HTTP

This serves both the webpage and SSE endpoint, so no CORS configuration is needed. 
the `/` route returns the UI page, and start button sends the `new EventStream("/events")` to the streaming response /events.

```python
import asyncio
import json

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse

app = FastAPI()


def sse_event(name: str, data: dict) -> str:
    # A blank line marks the end of each SSE event.
    return f"event: {name}\ndata: {json.dumps(data)}\n\n"


@app.get("/events")
async def events(request: Request):
    async def generate():
        try:
            for percentage in range(0, 101, 20):
                if await request.is_disconnected():
                    return

                yield sse_event(
                    "progress",
                    {"percentage": percentage},
                )

                if percentage < 100:
                    # Simulate asynchronous work.
                    await asyncio.sleep(1)

            yield sse_event(
                "complete",
                {"message": "Processing finished"},
            )
        finally:
            # Release any per-stream resources here.
            print("SSE stream ended")

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # Disable Nginx buffering.
        },
    )


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
<!doctype html>
<html lang="en">
<head><title>SSE progress demo</title></head>
<body>
  <h2>SSE progress demo</h2>
  <button id="start">Start</button>
  <button id="stop">Stop</button>
  <progress id="progress" max="100" value="0"></progress>
  <pre id="output"></pre>

  <script>
    let source = null;

    const output = document.getElementById("output");
    const progress = document.getElementById("progress");

    function closeStream() {
      if (source) {
        source.close();
        source = null;
      }
    }

    document.getElementById("start").onclick = () => {
      closeStream();
      output.textContent = "";
      progress.value = 0;

      // Opens an HTTP GET request and reads the event stream.
      source = new EventSource("/events");

      source.addEventListener("progress", (event) => {
        const data = JSON.parse(event.data);
        progress.value = data.percentage;
        output.textContent += `Progress: ${data.percentage}%\\n`;
      });

      source.addEventListener("complete", (event) => {
        const data = JSON.parse(event.data);
        output.textContent += data.message + "\\n";

        // Prevent EventSource from reconnecting after completion.
        closeStream();
      });

      source.onerror = () => {
        output.textContent += "Connection interrupted. Click Start to retry.\\n";

        // This demo deliberately disables automatic retries.
        closeStream();
      };
    };

    document.getElementById("stop").onclick = () => {
      closeStream();
      output.textContent += "Stopped\\n";
    };

    window.addEventListener("beforeunload", closeStream);
  </script>
</body>
</html>
"""
```

Below is example with python
fastapi_client.py
```python
import asyncio
import json

import httpx


async def main():
    # Allow the response stream to remain idle without a read timeout.
    timeout = httpx.Timeout(10.0, read=None)

    async with httpx.AsyncClient(timeout=timeout) as client:
        async with client.stream(
            "GET",
            "http://localhost:8000/events",
            headers={"Accept": "text/event-stream"},
        ) as response:
            response.raise_for_status()

            event_name = "message"
            data_lines = []

            async for line in response.aiter_lines():
                # A blank line ends an SSE event.
                if line == "":
                    if data_lines:
                        data = json.loads("\n".join(data_lines))

                        if event_name == "progress":
                            print(f"Progress: {data['percentage']}%")

                        elif event_name == "complete":
                            print(data["message"])
                            return  # Exiting the context closes the stream.

                        else:
                            print(f"Event: {event_name}, data: {data}")

                    event_name = "message"
                    data_lines = []
                    continue

                # SSE comments are often used as heartbeats.
                if line.startswith(":"):
                    continue

                field, separator, value = line.partition(":")
                if separator and value.startswith(" "):
                    value = value[1:]

                if field == "event":
                    event_name = value
                elif field == "data":
                    data_lines.append(value)


if __name__ == "__main__":
    asyncio.run(main())
```

### One FastMCP
1. server: mcp_server.py
```python
import asyncio
# **`Context` is a Python class representing the execution context of the current MCP request.** It gives your tool access to request information, the MCP session, and methods such as progress reporting.
from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP(
    "Progress Demo",
    host="127.0.0.1",
    port=8001,
    json_response=False,  # Enable streaming SSE responses.
)


@mcp.tool()
async def generate_report(report_name: str, ctx: Context) -> str:
    """Generate a report and send progress updates."""

    for step in range(1, 6):
        # Simulate asynchronous work.
        await asyncio.sleep(1)

        await ctx.report_progress(
            progress=step,
            total=5,
            message=f"Processing {report_name}: step {step}/5",
        )

    return f"Report '{report_name}' generated successfully."


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```
1. client: mcp_client.py
```python
import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def on_progress(
    progress: float,
    total: float | None,
    message: str | None,
):
    if total:
        percentage = progress / total * 100
        print(f"{percentage:.0f}% — {message}")
    else:
        print(f"Progress: {progress} — {message}")


async def main():
    async with streamablehttp_client(
        "http://127.0.0.1:8001/mcp"
    ) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "generate_report",
                arguments={"report_name": "Monthly Sales"},
                progress_callback=on_progress,
            )

            if result.isError:
                print("Tool failed:")

            for block in result.content:
                if block.type == "text":
                    print(block.text)


if __name__ == "__main__":
    asyncio.run(main())
```
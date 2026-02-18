Date: 2026-01-29
Course: https://www.tryexponent.com/courses/system-design-interviews/system-design-apis
Tags: [[API]] [[interview]] [[System Design Interview]]

# Content

## gRPC
gRPC (Google Remote Procedure Call) is a high-performance, open-source framework for building fast, language-agnostic, and secure microservices. Utilizing HTTP/2 for transport and Protocol Buffers (binary serialization) as the default interface definition language, it allows clients to invoke methods on remote servers as if they were local, supporting unary and streaming communication patterns. [[1](https://github.com/grpc/grpc)]

Key Features and Benefits
- Performance: Significantly faster than JSON/HTTP 1.1 due to smaller, binary Protocol Buffer payloads.
- HTTP/2 Based: Enables multiplexing, header compression, and bidirectional streaming.
- Strongly Typed Contracts: Defined using files, which auto-generate client/server code in multiple languages.
- Polyglot: Supports diverse programming languages including Go, Java, Python, C++, Node.js, and C#.
- Streaming: Supports client-side, server-side, and bidirectional streaming for real-time data. [[2](https://grpc.io/docs/what-is-grpc/faq/)]

Common Use Cases
- Microservices: Ideal for low-latency, high-throughput service-to-service communication.
- Polyglot Environments: Connecting services written in different languages.
- Mobile and IoT: Efficient for resource-constrained devices. [[3](https://www.youtube.com/watch?v=V5ZiNSMDE4E)]

Limitations
- Browser Support: Cannot be implemented directly in a browser; requires a proxy (gRPC-Web).
- Human Readability: Binary payload makes debugging more complex than text-based REST/JSON.
- Learning Curve: Requires understanding Protocol Buffers and HTTP/2 concepts.
#### Example:
1. Define the API in a `.proto`
```proto
// calculator.proto
syntax = "proto3";

package demo;

service Calculator {
  rpc Add (AddRequest) returns (AddReply) {}
}

message AddRequest {
  int32 a = 1;
  int32 b = 2;
}

message AddReply {
  int32 sum = 1;
}

```
2. Generate Python code
```bash
pip install grpcio grpcio-tools
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculator.proto
```
3. Server
```python
# server_grpc.py
from concurrent import futures
import grpc

import calculator_pb2
import calculator_pb2_grpc

class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def Add(self, request, context):
        return calculator_pb2.AddReply(sum=request.a + request.b)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server on :50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

```
4. Client
```python
# client_grpc.py
import grpc
import calculator_pb2
import calculator_pb2_grpc

def main():
    with grpc.insecure_channel("127.0.0.1:50051") as channel:
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        resp = stub.Add(calculator_pb2.AddRequest(a=7, b=8))
        print(resp.sum)  # 15

if __name__ == "__main__":
    main()

```


Server:
## JSON-RPC (Simple, HTTP-friendly RPC)
- Payload includes `method`, `params`, `id`
- Easy to implement, works well internally
#### Example:
Server:
```python
# server_jsonrpc.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any

app = FastAPI()

class JsonRpcRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Any | None = None
    id: int | str | None = None

@app.post("/rpc")
def rpc(req: JsonRpcRequest):
    try:
        if req.method == "add":
            a, b = req.params["a"], req.params["b"]
            result = a + b
        elif req.method == "health":
            result = {"status": "ok"}
        else:
            raise HTTPException(status_code=400, detail=f"Unknown method: {req.method}")

        return {"jsonrpc": "2.0", "result": result, "id": req.id}
    except Exception as e:
        return {"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}, "id": req.id}

```
Run: 
```sh
uvicorn server_jsonrpc:app --reload
```

Client:
```python
# client_jsonrpc.py
import requests

payload = {
    "jsonrpc": "2.0",
    "method": "add",
    "params": {"a": 10, "b": 32},
    "id": 1
}

resp = requests.post("http://127.0.0.1:8000/rpc", json=payload, timeout=10)
print(resp.json())  # {'jsonrpc': '2.0', 'result': 42, 'id': 1}

```


## XML-PRC (older but built into Python stdlib)
- RPC over HTTP using XML
- Useful for quick demos or legacy integrations

#### Example:
Server:
```python
# server_xmlrpc.py
from xmlrpc.server import SimpleXMLRPCServer

def add(a, b):
    return a + b

def health():
    return {"status": "ok"}

server = SimpleXMLRPCServer(("127.0.0.1", 8000), allow_none=True)
server.register_function(add, "add")
server.register_function(health, "health")

print("XML-RPC server on http://127.0.0.1:8000")
server.serve_forever()

```
Client:
```python
# client_xmlrpc.py
import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:8000", allow_none=True)

print(proxy.add(2, 3))        # 5
print(proxy.health())         # {'status': 'ok'}

```
## Thrift / Avro RPC / Other IDL-based PRC
Similar idea to gRPC; less common in new Python projects but still used
Example: invoking AWS Lambda function directly (still “call a function remotely”)

## Cloud "invoke" APIs (PRC-like)
# Note


# Reference


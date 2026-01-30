Date: 2026-01-29
Course: https://www.tryexponent.com/courses/system-design-interviews/system-design-apis
Tags: [[API]] [[interview

# Content

### What GraphQL is

GraphQL is an API style where the client sends a **query** (or **mutation**) that precisely describes **what data it wants**, and the server returns **exactly that shape**.

Key characteristics:

* **Single endpoint** (typically `/graphql`)
* **Strongly typed schema** (server publishes types and fields)
* Client controls **selection set** (fields to fetch)
* Great at fetching related data in one round trip

---

## When you should use GraphQL

Use GraphQL when:

* **Many different clients** (web, mobile, partners) need *different slices* of the same data
* You have lots of “resource relationships” (User → Orders → Items → Shipping) and want to avoid multiple calls
* You want a **self-documenting contract** with type system + introspection
* You need to evolve the API frequently without creating many REST versions/endpoints

GraphQL is especially good for:

* dashboards
* feed-style apps
* “profile pages” that assemble many components
* BFF (backend-for-frontend) layers

---

## When you should NOT use GraphQL

GraphQL can be the wrong tool when:

* You mostly do **simple CRUD** and caching with standard HTTP semantics matters a lot
* You need **simple operational visibility** (each endpoint = one business action)
* You have heavy “command-style” actions (RPC fits better)
* You have very high traffic and complex queries risk overloading backend (GraphQL needs guardrails: depth limits, complexity limits, query allowlists)

---

# A concrete GraphQL example (Python)

Below is a minimal example using **Strawberry** + FastAPI.

### Install

```bash
pip install fastapi uvicorn strawberry-graphql
```

### Server: `graphql_server.py`

```python
from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from dataclasses import dataclass
from typing import List, Optional

# ----- Fake in-memory data -----
@dataclass
class OrderModel:
    id: str
    total_cents: int

@dataclass
class UserModel:
    id: str
    name: str
    orders: List[OrderModel]

DB = {
    "u1": UserModel(
        id="u1",
        name="JC",
        orders=[OrderModel(id="o1", total_cents=2599), OrderModel(id="o2", total_cents=1099)],
    )
}

# ----- GraphQL types -----
@strawberry.type
class Order:
    id: str
    total_cents: int

@strawberry.type
class User:
    id: str
    name: str

    @strawberry.field
    def orders(self) -> List[Order]:
        # In real apps, fetch from DB/service
        return [Order(id=o.id, total_cents=o.total_cents) for o in DB[self.id].orders]

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: str) -> Optional[User]:
        u = DB.get(id)
        if not u:
            return None
        return User(id=u.id, name=u.name)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_order(self, user_id: str, total_cents: int) -> Order:
        u = DB[user_id]
        new_id = f"o{len(u.orders) + 1}"
        u.orders.append(OrderModel(id=new_id, total_cents=total_cents))
        return Order(id=new_id, total_cents=total_cents)

schema = strawberry.Schema(query=Query, mutation=Mutation)

app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")
```

Run:

```bash
uvicorn graphql_server:app --reload --port 8000
```

### Client query (Python): `graphql_client.py`

```python
import requests

url = "http://127.0.0.1:8000/graphql"

query = """
query GetUser($id: String!) {
  user(id: $id) {
    id
    name
    orders { id totalCents: total_cents }
  }
}
"""

resp = requests.post(url, json={"query": query, "variables": {"id": "u1"}})
print(resp.json())
```

### What this demonstrates

* Client asks for `user { id name orders { id total_cents } }` in **one call**
* Client can request fewer fields (only `name`), and server returns less

---

# Benefits vs REST API

Where GraphQL beats REST:

* Avoids **over-fetching / under-fetching** (REST often returns fixed payload shapes)
* Avoids many round trips for nested data (REST often needs `/users/1`, `/users/1/orders`, `/orders/xyz/items`)
* Strong typing + self-documentation; schema is a “source of truth”
* Great for UI-driven data needs (component-based frontends)

Where REST beats GraphQL:

* Simpler mental model and operations
* HTTP caching/CDN friendliness is easier (GET endpoints cache naturally)
* Monitoring/rate limiting per endpoint is straightforward
* Good for public APIs with stable resources and simple shapes

---

# Benefits vs RPC (gRPC/JSON-RPC)

Where GraphQL beats RPC:

* Better for **data graph fetching** (querying many related entities)
* Client-driven payload shape (RPC responses are usually fixed by method)
* Great as a BFF layer that aggregates multiple services

Where RPC beats GraphQL:

* Better for **actions/commands**: `ChargeCard`, `ApproveLoan`, `ReindexSearch`
* Lower overhead and typically simpler backend execution
* gRPC in particular is excellent for service-to-service performance + streaming + strong contracts

A good rule:

* **GraphQL** = “give me exactly this data shape”
* **RPC** = “do this operation”
* **REST** = “manage these resources via standard HTTP verbs”

---

## Practical architecture tip (common in real systems)

Many teams do:

* **GraphQL for frontend** (BFF / API gateway)
* Behind it, services talk via **gRPC or REST**
* Payments/commands often stay **RPC-like** even if exposed through GraphQL (as mutations)

---

If you tell me your scenario (frontend needs to assemble resume/work experience/projects from multiple tables/services? or internal microservices?), I can recommend whether GraphQL actually helps and show a schema design that won’t turn into an “N+1 query” problem.



# Note


# Reference


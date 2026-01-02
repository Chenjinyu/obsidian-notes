Date: 2025-10-26
Course:
Tags: [[Base Knowledge]] 
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content
# START
## Situlation
I have a distributed web applications, which route the request to differnet backen services by either ALB or Niginx proxy.
If i want to have multi-requiests and won't lose my shipping car, perference info, etc. you can use the sticky session provided by ALB. 

### Sticky Session 
(also called session affinity) is a load blabacing feature that ensures that all requests from the same client are always routed to the same backend server(or target) during a session.

#### How sticky sessions work
1. Cookie-based affinity:
The load balancer inserts a cookie (e.g., AWS ALB’s AWSALB cookie or Nginx’s custom cookie). When the client sends requests, the cookie tells the load balancer which backend server to route to.
2. Source IP affinity:
The load balancer maps the client’s IP to a backend server. Future requests from that IP are always routed to the same server.

#### Example
Imagine 3 backend servers behind a load balancer:
- Without sticky sessions:
  - Request 1 → Server A
  - Request 2 → Server B (session lost if stored in Server A’s memory)
- With sticky sessions:
  - Request 1 → Server A
  - Request 2 → Server A (same session preserved)

#### Pros
- Easy way to maintain user session state without redesigning the application.
- Works well for stateful legacy apps.
#### Cons
- Uneven load distribution: Some servers may get overloaded if too many clients stick to them.
- Scalability issues: Harder to scale horizontally.
- Server dependency: If a server fails, sticky sessions break unless session data is replicated elsewhere.

> Modern best practice: Instead of relying on sticky sessions, applications usually store session state in shared storage (e.g., Redis, DynamoDB, Memcached, or databases), making the app stateless so any server can handle requests.

### A Shared Storage (Reids, DynamoDB, Memcached, or Postgres, etc)
When you avoid **sticky sessions**, you make your application **stateless**. That means:
* The **load balancer** can route each request to *any* healthy server.
* The **session data** is stored in a **shared external storage** instead of the server’s RAM.
* Any server can then read the session info from this **shared storage** to continue the user’s session.

#### How shared storage solves the problem

##### 1. **User logs in**
* User → Load Balancer → Server A
* Server A authenticates the user and creates a session (e.g., `session_id=12345`).
* Server A stores session data (`user_id`, roles, preferences, cart items, etc.) in **shared storage**:
  * Could be **Redis**, **Memcached**, **DynamoDB**, **PostgreSQL/MySQL**, etc.
* Server A sends back a **session token/cookie** to the client (e.g., JWT or session ID).

##### 2. **User makes another request**

* User → Load Balancer → Server B (randomly chosen, no sticky session).
* Server B looks at the **session token** (from cookie or header).
* Server B fetches session data from shared storage using that token/session ID.
* Server B now knows the user is logged in and can continue serving without missing context.

##### 🔹 Example with Redis as shared storage

* **Server A**:
  ```python
  session_id = "abc123"
  redis.set(session_id, {"user_id": 42, "cart": ["item1", "item2"]}, ex=3600)
  response.set_cookie("session_id", session_id)
  ```
* **Server B** (on next request):
  ```python
  session_id = request.cookies.get("session_id")
  session_data = redis.get(session_id)  # {"user_id": 42, "cart": ["item1", "item2"]}
  ```
##### Benefits of shared storage
- Any server can serve any request (scales horizontally).
- Session survives even if one server crashes.
- Easier auto-scaling in cloud (new servers can immediately handle users).

##### Downsides

- ⚠️ More complexity (need to manage Redis/DB).
- ⚠️ Potential performance bottleneck if storage isn’t tuned for high throughput.
- ⚠️ Slightly higher latency vs in-memory local session.


> That’s why many modern systems use **stateless authentication with JWTs** (JSON Web Tokens) stored in cookies/headers. With JWTs, session state is encoded into the token itself, so the server doesn’t even need to hit a shared storage for every request.


### Redis-backed sessions vs JWT-based stateless sessions and comparsion.
Perfect! Let’s break down **Redis-backed sessions** vs **JWT-based stateless sessions** and compare them clearly.

#### 1. **Redis-backed Sessions (Server-side sessions)**

##### 🔹 How it works:

1. User logs in → server authenticates.
2. Server generates a **session ID** (random token) and stores **session data** in Redis:

   ```json
   {
     "session_id": "abc123",
     "user_id": 42,
     "roles": ["admin"],
     "cart": ["item1", "item2"]
   }
   ```
3. Server sends **session ID** to client as a cookie.
4. On each request, any server retrieves session data from Redis using session ID.

##### 🔹 Pros:

* Full control over session data (can update, delete, invalidate at any time).
* Session can store **large, complex state** easily.
* Can immediately revoke session (delete from Redis).

##### 🔹 Cons:

* Requires **extra infrastructure** (Redis/Memcached).
* Extra network call to storage → slight latency.
* Scalability depends on Redis performance.

#### 2. **JWT-based Sessions (Client-side stateless sessions)**

##### 🔹 How it works:
1. User logs in → server authenticates.
2. Server generates a **JWT** (JSON Web Token) containing user info or claims:

   ```json
   {
     "sub": "42",
     "roles": ["admin"],
     "exp": 1715600000
   }
   ```
3. Server signs the JWT with a secret key and sends it to the client (cookie or header).
4. On each request, server **verifies JWT signature** and extracts user info—no need for server-side storage.

##### 🔹 Pros:

* Fully **stateless**, no Redis or DB calls required.
* Scales horizontally perfectly; any server can verify the JWT.
* Reduced latency (no round-trip to shared storage).

##### 🔹 Cons:

* Can’t easily revoke a JWT until it expires (unless you implement a token blacklist).
* Sensitive info should not be stored inside JWT (or should be encrypted).
* Token size can grow if you store too much data inside.

#### 3. **Side-by-Side Comparison**

| Feature            | Redis-backed Session          | JWT Stateless Session                                              |
| ------------------ | ----------------------------- | ------------------------------------------------------------------ |
| Storage            | Server-side (Redis/DB)        | Client-side (token)                                                |
| Scalability        | Requires shared storage       | Fully stateless, easy to scale                                     |
| Session Revocation | Immediate (delete from Redis) | Only via blacklist or expiry                                       |
| Latency            | Extra network call            | Minimal, verify signature only                                     |
| Data Size          | Can store large session       | Keep token small (<1-2KB recommended)                              |
| Security           | Secret stored on server       | Signature must be secure; data visible in payload if not encrypted |

#### ✅ Summary

* **Use Redis-backed sessions**:

  * When session data is **large or complex**
  * When you need **instant revocation**
  * Suitable for traditional stateful apps

* **Use JWT stateless sessions**:

  * When you want **fully stateless scalable apps**
  * Ideal for **microservices & cloud-native APIs**
  * Can combine with **short-lived tokens + refresh tokens** for security


## Tasks
> Analaysis which method from sticky session, shared storaged, or JWT token is the best solution. 

## Action


## Resolve


## Takeaways


# Note


# Reference


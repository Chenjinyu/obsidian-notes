The **`access_token`** is what you normally use as the Bearer token when calling an API.

```
POST /orders
Authorization: Bearer <access_token>
```

The **`refresh_token` should NOT be sent to your business API**. Its purpose is to obtain a new access token when the current access token expires.

For example, FedSSO might return:

```
{
  "access_token": "eyJ...",
  "refresh_token": "abc123...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

The lifecycle is:

```
Login / Authorization
        │
        ▼
      FedSSO
        │
        ├── access_token
        │       │
        │       └──────► POST /orders
        │                Authorization: Bearer <access_token>
        │
        └── refresh_token
                │
                │ access_token expires
                ▼
          /token.oauth2
                │
                │ grant_type=refresh_token
                │ refresh_token=<refresh_token>
                ▼
             FedSSO
                │
                ▼
         New access_token
```

So if the access token expires, the client could make something conceptually like:

```
POST /as/token.oauth2
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token
&refresh_token=<refresh_token>
```

FedSSO then returns a new access token.

A simple way to remember:

```
access_token
    ↓
Give to API
    ↓
Authorization: Bearer <access_token>


refresh_token
    ↓
Give ONLY to authorization/token server
    ↓
Get a new access_token
```

One nuance: `Bearer` describes **how a token is presented**, and OAuth token endpoints can use refresh tokens as credentials in the refresh flow. But when people say **“put the Bearer token in the API request”**, they mean the **access token**, not the refresh token.

Also, **Client Credentials app-to-app flows typically don't return a refresh token**. Service A can simply use its `client_id` + `client_secret` to request another access token when needed.

---

It doesn't happen automatically just because you have a `refresh_token`. **Your Python client code or an OAuth library must detect that the access token is expired/near expiry and call FedSSO's token endpoint using the refresh token.**

For example, imagine FedSSO originally returned:

```
{
    "access_token": "ACCESS_ABC",
    "refresh_token": "REFRESH_XYZ",
    "expires_in": 3600,
    "token_type": "Bearer"
}
```

Your Python client could do this:

```python
import requests
import time

TOKEN_URL = "https://fedsso.example.com/as/token.oauth2"

client_id = "my-client"
client_secret = "my-secret"

access_token = None
refresh_token = None
expires_at = 0


def refresh_access_token():
    global access_token, refresh_token, expires_at

    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        },
        auth=(client_id, client_secret)
    )

    response.raise_for_status()
    token = response.json()

    access_token = token["access_token"]

    # Some providers rotate refresh tokens
    if "refresh_token" in token:
        refresh_token = token["refresh_token"]

    expires_at = time.time() + token["expires_in"]


def get_access_token():
    # Refresh 60 seconds before expiration
    if time.time() >= expires_at - 60:
        refresh_access_token()

    return access_token
```

Then your API call doesn't need to care about refreshing:

```python
def create_order(order):
    token = get_access_token()

    response = requests.post(
        "https://api.example.com/orders",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json=order
    )

    return response.json()
```

So the flow becomes:

```
Python Client
     │
     │ get_access_token()
     ▼
Is access token expired/almost expired?
     │
   ┌─┴───────────────┐
   │ NO              │ YES
   ▼                 ▼
Use existing     POST /token.oauth2
access token
                 grant_type=refresh_token
                 refresh_token=xxxxx
                       │
                       ▼
                    FedSSO
                       │
                       ▼
                new access_token
                       │
              save new expiration
                       │
                       ▼
                  POST /orders
                       │
        Authorization: Bearer
              <new_access_token>
```

### A better production approach

Usually you don't want to write all of this token management yourself. An OAuth/OIDC library can handle token expiration and refreshing.

For example, with `requests-oauthlib`, the pattern is roughly:

```python
from requests_oauthlib import OAuth2Session

def token_updater(new_token):
    # Store this securely:
    # database / encrypted token store / etc.
    save_token(new_token)


oauth = OAuth2Session(
    client_id,
    token=stored_token,
    auto_refresh_url=TOKEN_URL,
    auto_refresh_kwargs={
        "client_id": client_id,
        "client_secret": client_secret
    },
    token_updater=token_updater
)

response = oauth.post(
    "https://api.example.com/orders",
    json={
        "product_id": "ABC123",
        "quantity": 2
    }
)
```

Then conceptually the library does:

```
oauth.post("/orders")
        │
        ▼
Check access_token
        │
   expired?
    /      \
  NO        YES
  │          │
  │       refresh_token
  │          │
  │       FedSSO
  │          │
  │     new access_token
  │          │
  └────┬─────┘
       ▼
POST /orders
Authorization: Bearer <access_token>
```

One other distinction matters for your FedSSO work: if you're doing **app-to-app Client Credentials**, you usually **don't need a refresh token at all**. When the access token expires, the application simply authenticates again with its `client_id`/`client_secret` and requests another access token:

```
User/OIDC flow:
access_token expires
        ↓
refresh_token
        ↓
new access_token


App-to-app Client Credentials:
access_token expires
        ↓
client_id + client_secret
        ↓
new access_token
```

That distinction is useful because the token you showed earlier—with `client_id` and `sub` both representing the application—looks consistent with the kind of token you may encounter in an app-to-app flow.
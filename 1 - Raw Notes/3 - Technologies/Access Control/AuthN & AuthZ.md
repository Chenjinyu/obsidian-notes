Date: 2025-10-26
Course:
Tags: [[../../../3 - Zettelkasten/B - Tags/Terminology]] [[../../../3 - Zettelkasten/B - Tags/Base Knowledge]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content

OAuth 2.0 & OpenID Connect

## 🧩 Short answer first
- **OpenID Connect (OIDC)** = for **authentication** → _“Who is this user?”_  (The OIDC built on top of OAuth 2.0)
- **OAuth 2.0** = for **authorization** → _“Can this app access this resource?”_
- **Token validation/introspection** = Is this credential valid, and what does it say you're allowed to do?
- Identity provider(IdP) = a service/system responsible for establishing a user's identity. 
They share the **same mechanics** (redirects, tokens, scopes, authorization code flow),  
but what they **issue** and **validate** differs.


---

## 🧠 The conceptual difference

| Protocol           | Purpose                                                   | Audience                     | What you get                 | Standard Format                     | Typical Contents                                      | Typical Use Case                      |
| ------------------ | --------------------------------------------------------- | ---------------------------- | ---------------------------- | ----------------------------------- | ----------------------------------------------------- | ------------------------------------- |
| **OpenID Connect** | Authentication (Login) protocol built on top of OAuth 2.0 | your application             | `id_token`(ID Token)         | always a JWT                        | User's identity details (sub, name, email, auth_time) | Log in user via Microsoft/Google/Okta |
| **OAuth 2.0**      | Authorization (Access control)                            | the resource server(the API) | `access_token`(Access Token) | Opaque string(random text) or a JWT | Scopes(read, write) and internal API date             | Let app access protected APIs or data |
## Authentication & Authorization Server are the IdP
1. Microsoft Entra ID
2. PingFederate
3. Okta
4. OAuth0 (Its not OAuth 2.0 which is authorization framework)
5. or an enterprise FedSSO system

### An IdP can support different protocols, such as:
```text
                       IdP
                        │
       ┌────────────---─┼────────────────────┐
       │                │                    │
      OIDC(AuthN)    SAML(AuthN)    OAuth 2.0(AuthZ)
      

an IdP is a system/role, and it _may support_ OIDC and OAuth 2.0. They aren't literally “inside” every IdP.
so, if someone says `we use an IdP`, but does not mean which protocl is being used.
```

for the FedSSO and any other IdP, it could involve password, MFA, an existing SSO session, and certificate, etc. 

### Authorization
```text
JC
 ↓
Client application
 ↓
request:
    scope=employee.read
    resource=employee-api
 ↓
FedSSO decides whether that access can be granted
```

> Authentication frequently happens as part of an authorization flow, but you shouldn't think of authorization as simply a second endpoint that always runs “after authentication.”


### The Authentication & Authorization Flow

```text
                            OAuth 2.0 / FedSSO
                                      │
          ┌───────────────────────────┴──────────────────────────┐
          │                                                      │
     USER LOGIN                                            APP-TO-APP
          │                                                      │
 Authorization Code                                         Client Credentials
          │                                                      │
/authorization.oauth2 (scope=openid order.read)                  │
          │                                                      │
    user logs in                                                 │
          │                                                      │
          ▼                                                      ▼
       Authorization code                                  client_id + secret
          │                                                       │
          └────────────────────────────┬──────────────────────────┘
                                       ▼
                           /token.oauth2  -> POST /as/token.auth2, grant_type=client_credentials&client_id=x&client_secret=x&scope=employe.read (ONLY when request authorization, need to provide scope)
                                       │
                                  Access Token (bearer token)
                                       │
                                       ▼
                                      API (add bearer token in the API header, and do optional check with introsepct.auth2)
                                       │
                               optionally checks
                                       │
                                       ▼
                              /introspect.oauth2
```

```text
                REQUESTING TOKEN
                =================

USER LOGIN                         APP-TO-APP

/authorization.oauth2                 /token.oauth2
        │                                      │
scope=openid (for user)                    grant_type=
      profile                              client_credentials
      order.read                               │
        │                                scope=order.read
        ▼                                      │
   User login                                  │
        │                                      │
        ▼                                      │
Authorization Code                             │
        │                                      │
        ▼                                      ▼
   /token.oauth2                         Access Token
        │                                      │
        ▼                                      │
 ID Token + Access Token                       │
        │                                      │
        └──────────────────┬───────────────────┘
                           │
                           ▼
                      CALLING API
                      ===========

                   POST /api/orders

           Authorization: Bearer <access_token>

                           │
                           ▼
                          API
                           │
                 validates token
                           │
                 ┌─────────┴──────────┐
                 │                    │
                aud                 scope
                 │                    │
          "Is token for me?"    "Can caller
                              write orders?"
```

```text
                  Client
                     │
                     │ POST /api/orders
                     │ Authorization: Bearer <access_token>
                     ▼
     ┌───────────────────────────────┐
     │         Python API            │
     │                               │
     │  1. Is token present?         │
     │  2. Verify signature          │ -> Was it really issued/signed by FedSSO?
     │  3. Check exp                 │ -> Has it expired?
     │  4. Check iss                 │ -> Did it come from the expected FedSSO?
     │  5. Check aud (if applicable) │ -> Was it intended for this API?
     │  6. Check required scope      │ -> is this operation permitted?
     │                               │
     │        All valid?             │
     │           │                   │
     │          YES                  │
     │           ▼                   │
     │    Execute API logic          │
     └───────────────────────────────┘
```

```python
from fastapi import FastAPI, Header, HTTPException
import jwt

app = FastAPI()

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
...
-----END PUBLIC KEY-----"""

EXPECTED_ISSUER = "https://fedsso.example.com"
EXPECTED_AUDIENCE = "order-api"


def validate_access_token(
    authorization: str,
    required_scope: str
):
    # 1. Check Authorization header
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing Bearer token"
        )

    token = authorization.removeprefix("Bearer ").strip()

    try:
        # 2. Validate JWT
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            issuer=EXPECTED_ISSUER,
            audience=EXPECTED_AUDIENCE
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    # 3. Check authorization scope
    scopes = payload.get("scope", "")

    # Some providers return a string:
    # "order.read order.write"
    if isinstance(scopes, str):
        scopes = scopes.split()

    if required_scope not in scopes:
        raise HTTPException(
            status_code=403,
            detail=f"Missing required scope: {required_scope}"
        )
    return payload


@app.post("/orders")
def create_order(
    order: dict,
    authorization: str = Header(None)
):
    claims = validate_access_token(
        authorization,
        required_scope="order.write"
    )
    # Token has passed authentication + authorization.
    # Now execute business logic.
    return {
        "message": "Order created",
        "order": order,
        "subject": claims.get("sub")
    }
```

[1] User opens app
     ↓   -> The frontend app detects if the user has active session or valid token, if not, redirect to authentication/login page.
        -> the client_id is the **public identifier** for the web application that registered with the Authorization server. it tells the identity provider which app is asking for access
        -> the response_type is code, which means return the authentication code back, which will be expired for determined time.
        -> the presence of `openid` means OpenID Connect is being used.
        
```
https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize?
  client_id={frontend_client_id} # YOUR_APP_CLIENT_ID
  &response_type=code
  &redirect_uri=https://app.company.com/auth/callback
  &scope=openid profile email api://{backend_api_client_id}/.default
  &state={random_string}
```

[2] Redirect to Azure AD login (oauth2/v2.0/authorize)
     ↓   -> check the user if has the access login/ or the Azure AD server can find the correct records associate with the user. if yes, then go to 2-factor authentication page
        -> Use OpenID Connect to identify who logged in / who you are
        -> 
[3] Azure AD authenticates user (SSO/MFA)
     ↓ -> like use Authentication app / yubikey, etc
[4] Redirects back with authentication code
     ↓ -> once the SSO && MFA success, it returns the {authentication_code},   
       -> the {authentication_code} includes in step 5's header and send to backend
[5] Frontend exchanges code → access_token + id_token
     ↓ -> the frontend (or its BFF - backend for frontend) sends a POST to Azure AD's token endpoint
    the 
```
POST https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token
Content-Type: application/x-www-form-urlencoded

client_id={frontend_client_id}
&grant_type=authorization_code
&code={authorization_code}
&redirect_uri=https://app.company.com/auth/callback
&code_verifier={pkce_verifier}
```

it returns JWT token
the server returns the id_token which contains user identity info (subject, email, name, etc)
the access_token, used to call APIs (authorizes resource access)
```
{
  "access_token": "<JWT access token>",
  "id_token": "<JWT ID token>",
  "refresh_token": "<refresh token>",
  "expires_in": 3600
}
```
depending on the application, those tokens can include group claims or app role claims
```
{
  "aud": "your-api-client-id",
  "sub": "8a59bda0-1234-4bcd-a7cd-909090909090",
  "name": "Jane Smith",
  "email": "jane.smith@contoso.com",
  "roles": ["Admin", "FinanceViewer"],
  "groups": [
    "a3f3e7b3-2222-44cc-bb33-4d5dd9eeab44",
    "b8e73c91-9d22-45d2-9999-0d7f0cba1a12"
  ]
}
```
[6] Frontend → API request with access_token
     ↓ -> the frontend attaches the <access_token> in the Authorization header to the backend
```
GET /api/orders
Authorization: Bearer <access_token>
```

[7] Backend validates token with Azure AD public keys
     ↓ -> the backend validate the JWT signature (using Microsoft's public keys / JWKS)
       -> Check claims in the JWT by decodes it
       -> check the `group` and `role` to decide access
```
{
  "aud": "your-api-client-id",
  "sub": "8a59bda0-1234-4bcd-a7cd-909090909090",
  "name": "Jane Smith",
  "email": "jane.smith@contoso.com",
  "roles": ["Admin", "FinanceViewer"],
  "groups": [
    "a3f3e7b3-2222-44cc-bb33-4d5dd9eeab44",
    "b8e73c91-9d22-45d2-9999-0d7f0cba1a12"
  ]
}
```
	**aud** (audience) matches the backend’s app registration client ID or API scope
	 **exp** (expiration) is still valid
	**iss** (issuer) matches the tenant’s URL
	**scp** or role or groups for authorization

   -> (Optional) If needed, call Microsoft graph to get group membership if not included in token claims
scp or roles or groups for authorization
[8] Backend checks AD groups/roles
     ↓ -> it maps AD groups to permissions:
 ```
{
  "oid": "user-object-id",
  "name": "JC",
  "groups": ["group-id-1", "group-id-2"]
}

```
[9] (Optional) Backend calls Graph or other API using client credentials. 
     ↓ -> the backend server also needs to call authentication endpoint to identity the web application/backend server has the correct access by providing client_id and client_secret.
       -> the Azure AD reponds as below:
```
{
  "access_token": "<service_access_token>",
  "token_type": "Bearer"
}
```

[10] Backend returns response by
   -> Token is valid
   -> User is in required AD group
[11] Backend denied the access as the otherwise
   -> Invalid Token -> 401 Unauthorized
   -> valid token, insufficient group -> 403 Forbidden 
   
| Token                    | Purpose                             | Used by            |
| ------------------------ | ----------------------------------- | ------------------ |
| **ID Token**             | Identifies the user (login session) | Frontend           |
| **Access Token**         | Authorizes API calls                | Frontend → Backend |
| **Refresh Token**        | Renew access tokens silently        | Frontend           |
| **Service Access Token** | Machine-to-machine API access       | Backend            |
|                          |                                     |                    |
|                          |                                     |                    |
### 🧩 TL;DR

* Azure AD knows which groups/roles a user belongs to.
* It encodes those memberships into the user’s **token**.
* Your backend reads those claims to determine what the user can access.
* You can manage all access control centrally in Azure AD — no separate user DB needed.
# Note


# Reference


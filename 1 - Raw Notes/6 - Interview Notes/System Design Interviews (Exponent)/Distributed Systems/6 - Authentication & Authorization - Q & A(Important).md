Date: 2026-02-17
Course:
Tags: [[System Design Interview]] [[Distributed System]] 

# Summary: OAuth2, OIDC, and Authentication/Authorization Q&A

---
## Q1: What OAuth2 grant types exist besides `client_credentials`?

**Answer:**

|Grant Type|Use Case|Status|
|---|---|---|
|**client_credentials**|Server-to-server, no user|✅ Active|
|**authorization_code**|Web apps, user login via browser redirect|✅ Active (recommended)|
|**password**|User sends username/password directly to app|⚠️ Deprecated (legacy only)|
|**refresh_token**|Exchange refresh token for new access token|✅ Active|
|**implicit**|Old SPA flow, token in URL|❌ Deprecated (use auth code + PKCE)|
|**device_code**|Devices without browsers (TVs, CLI tools)|✅ Active|
|**PKCE**|Security extension for mobile/SPA|✅ Active (use with auth code)|

---

## Q2: Can a client get a token without specifying scopes? How does the backend use it?

**Answer:**

**Yes**, a client can request a token without custom scopes. The token will contain only default scopes (like `openid`, `profile`, `email`), but NOT your custom `ro`/`rw` scopes.

**How the backend uses tokens:**

1. **Validates signature** using the auth server's public key (JWTs are signed, not encrypted)
2. **Reads the `scope` claim** directly from the JWT (it's plaintext JSON)
3. **Checks if required scope exists** — if missing, rejects the request

**Key point:** The scope is already inside the token when issued. Your backend doesn't "decrypt to determine access" — it reads the plaintext claims and enforces authorization rules.

If the client didn't request `rw` scope, the auth server won't include `rw` in the token, and your `@require_scope("rw")` check will fail.

---

## Q3: What is OIDC? Is it a framework? Where is it hosted?

**Answer:**

**OIDC (OpenID Connect)** is a **protocol/specification**, not a framework. It's an **identity layer built on top of OAuth2**.

**Formula:** OAuth2 + identity = OIDC

**Where is it hosted?**

OIDC itself isn't hosted — it's a standard (like HTTP). What gets hosted is an **OIDC Provider** (IdP):

- Keycloak (self-hosted)
- Auth0, Okta, Azure AD (SaaS)
- Google Identity, AWS Cognito

These servers implement the OIDC specification.

---

## Q4: OAuth2 vs OIDC — What's the difference? Why does OIDC return `access_token` if it's about authentication?

**Answer:**

### The Confusion Clarified

**OIDC doesn't replace OAuth2** — it **extends** it. OIDC is OAuth2 with an identity layer added.

||OAuth2|OIDC|
|---|---|---|
|**Purpose**|Authorization (what can you access?)|Authentication (who are you?) + Authorization|
|**Returns**|`access_token`|`access_token` + `id_token`|
|**Use case**|App calls API on user's behalf|App needs to know who logged in|

### What Each Token Does

|Token|Purpose|Used By|Contains|
|---|---|---|---|
|**`access_token`**|Authorization — what resources you can access|Backend API|`scope`, `permissions`, `exp`|
|**`id_token`**|Authentication — who you are|Frontend app|`sub`, `email`, `name`, `groups`|

### Why OIDC Returns Both

**Without OIDC (OAuth2 only):**

- Get `access_token` with scopes (`ro`, `rw`)
- Can call APIs, but **don't know WHO the user is**

**With OIDC:**

- Get `access_token` (same as OAuth2 — for API authorization)
- Get `id_token` (NEW — tells frontend "this is Alice, alice@example.com")

**OIDC includes authorization via `access_token` PLUS authentication via `id_token`.**

---

## Q5: Is `client_credentials` OAuth2-only? Does user login require `openid` scope and use OIDC?

**Answer:**

**✅ YES — You understood this perfectly!**

### Client Credentials Flow (Server-to-Server)

- **Uses:** OAuth2 only (not OIDC)
- **No human user** involved
- **Request:** `grant_type=client_credentials`, `scope=ro rw`
- **Returns:** `access_token` only (NO `id_token`)
- **Why no `id_token`?** No human identity — just service-to-service

### User Login Flow (Authorization Code / Password)

- **Uses:** OIDC (OAuth2 + identity)
- **Human user** involved
- **Request:** `grant_type=authorization_code`, `scope=openid email ro rw`
- **The `openid` scope triggers OIDC protocol**
- **Flow:**
    1. User redirected to IdP (Keycloak, Google, etc.)
    2. IdP authenticates user (checks password)
    3. Returns **both tokens:**
        - `access_token` — scopes for API (`ro`, `rw`)
        - `id_token` — user identity (`sub`, `email`, `name`)

### The Trigger: `openid` Scope

|Scope|Result|
|---|---|
|`scope=ro rw`|OAuth2 → only `access_token`|
|`scope=openid ro rw`|OIDC → `access_token` + `id_token`|

---

## Q6: Where are AD groups checked? Where is user profile stored? Is `scope=openid profile email ro rw` valid?

**Answer:**

### Where Authentication & Groups Are Checked

```
User enters credentials
    ↓
OIDC Provider (Keycloak, Okta, etc.)
    ↓
Connects to User Directory:
    - Internal DB (Keycloak's own database)
    - LDAP / Active Directory (corporate directory)
    - External IdP (Google, Azure AD, etc.)
    ↓
Returns:
    - Authentication result (password valid?)
    - User attributes (name, email, department)
    - Groups (Engineering, Finance, Admin)
    ↓
OIDC Provider puts groups in token claims
```

### In Keycloak with Active Directory

**Configuration:**

- Navigate to **User Federation** → Add **LDAP** provider
- Configure AD connection (host, bind DN, credentials)
- Use **Mappers** to map AD groups → JWT claims

**Flow:**

```
User login → Keycloak → LDAP query to AD
                           ↓
                    AD returns user + groups
                           ↓
                    Keycloak issues token with groups
```

### Where User Profile Is Stored

|Storage|Provides|
|---|---|
|Keycloak DB|Users created in Keycloak directly|
|LDAP/AD|Corporate directory (synced)|
|External IdP|Google/Azure profile data|

### Is `scope=openid profile email ro rw` Valid?

**YES! Perfectly valid.**

|Scope|Adds to `id_token`|
|---|---|
|`openid`|**Required** for OIDC, adds `sub` (user ID)|
|`profile`|Adds `name`, `given_name`, `family_name`, `picture`|
|`email`|Adds `email`, `email_verified`|
|`ro`|Custom scope for `access_token` (API authorization)|
|`rw`|Custom scope for `access_token` (API authorization)|

**Result:**

```json
// id_token (identity claims)
{
  "sub": "user123",
  "name": "Alice Smith",
  "email": "alice@company.com",
  "email_verified": true,
  "groups": ["engineering", "admin"]
}

// access_token (authorization)
{
  "scope": "openid profile email ro rw",
  "sub": "user123"
}
```

---

## Complete Authentication Flow Summary

```
1. User clicks "Login"
2. Redirected to Keycloak (OIDC Provider)
3. User enters username + password
4. Keycloak queries Active Directory (LDAP):
   ✓ Password correct?
   → User groups: ["engineering", "admin"]
   → Email: alice@company.com
5. Keycloak issues tokens:
   - id_token: name, email, groups (for frontend display)
   - access_token: scopes ro, rw (for API authorization)
6. Frontend receives both tokens:
   - Reads id_token → displays "Welcome, Alice Smith"
   - Sends access_token to backend API
7. Backend API:
   - Validates access_token signature (using public key)
   - Checks scope contains "rw"
   - Allows/denies the request
```

---

## Key Takeaways

1. **OAuth2** = authorization protocol (scopes, what you can access)
2. **OIDC** = OAuth2 + authentication (adds identity via `id_token`)
3. **`openid` scope** = triggers OIDC, without it you only get OAuth2
4. **OIDC Provider** = the server (Keycloak, Okta) that implements the protocols
5. **IdP/User Directory** = where passwords and groups live (AD, LDAP, or internal DB)
6. **`access_token`** = for backend APIs (authorization)
7. **`id_token`** = for frontend apps (authentication, display user info)

# Note


# Reference


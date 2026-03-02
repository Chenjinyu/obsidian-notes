Date: 2026-02-17
Course:
Tags: [[../../../../7 - JCUS.LINK/System Design]] [[Distributed System]]

# Pre-Requirements

## Where to Create Client ID/Secret and Scopes
You have a few options depending on your setup:
**If you use a managed Identity Provider (recommended for production):**
- **Keycloak** (self-hosted, free) - Create a "Client" in your realm, define custom scopes there
- **Okta / Auth0** - Create an "Application" (machine-to-machine), define API scopes in the API settings
- **Azure AD** - Register an "App Registration", define "App Roles" or "OAuth2 permissions"

**If you want to manage it yourself (what we'll build below):**
- Your own Auth Server stores client credentials in a database
- You define scopes in config or DB
- You issue and validate JWTs yourself using a library like `python-jose` or `PyJWT`

# OAuth2 / OIDC Auth System — Quick Start

## Install dependencies

```bash
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] python-multipart httpx
```

## Run both servers

```bash
# Terminal 1 — Auth Server (AuthN + token issuer)
uvicorn auth_server:app --port 8000 --reload

# Terminal 2 — Resource Server (your actual API)
uvicorn resource_server:app --port 8001 --reload

# Terminal 3 — Run the demo
python demo_client.py
```

## Explore the APIs

- Auth Server docs: http://localhost:8000/docs
- Resource Server docs: http://localhost:8001/docs

---

## Flow Map → Code Reference

|Step|What happens|Where in code|
|---|---|---|
|0|Register client (get client_id + secret)|`POST /admin/register-client` in auth_server.py|
|1|Client sends credentials|`demo_client.py` POST requests|
|2|Server verifies identity|`hmac.compare_digest()` in auth_server.py|
|3|MFA (not shown — add TOTP here)|Extend `/token/login` in auth_server.py|
|4|Fetch groups from IdP|`USERS_DB` lookup (mock), replace with LDAP/Okta call|
|5-6|Build + issue JWT tokens|`_create_access_token()`, `_create_id_token()` in auth_server.py|
|7|API request with Bearer token|`headers = {"Authorization": f"Bearer {token}"}`|
|8|Validate token|`validate_token()` in resource_server.py|
|9|Extract claims|`claims = jwt.decode(...)`|
|10 RBAC|Role/scope check|`require_scope()`, `require_role()` decorators|
|10 ABAC|Attribute policy check|`abac_check()` in resource_server.py|
|10 ACL|Per-resource permission check|`acl_check()` calls `/acl/` on auth server|

## Pre-configured Test Accounts

|User|Password|Roles|Scopes|Groups|
|---|---|---|---|---|
|alice|password123|admin|ro, rw, admin|engineering, admin-group|
|bob|bobpass|viewer|ro|read-only-group|
|service-client-001|my-super-secret-value|service_reader, service_writer|ro, rw|—|

## Production Checklist

- [ ] Switch from HS256 to RS256 (asymmetric keys) — resource servers can verify without shared secret
- [ ] Use bcrypt for passwords, not sha256
- [ ] Store client secrets hashed in DB
- [ ] Add Redis for refresh token store (not in-memory dict)
- [ ] Add rate limiting on `/token/*` endpoints
- [ ] Add real IdP federation (LDAP, Okta, Azure AD)
- [ ] Replace `time_restricted` mock in ABAC with OPA (Open Policy Agent)
- [ ] Use HTTPS everywhere
- [ ] Rotate signing keys periodically


# Note


# Reference


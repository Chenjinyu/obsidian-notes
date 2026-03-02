![](assets/1%20-%20Keycloak%20Guide%20-%20HTML/file-20260217012941486.png)
![](assets/1%20-%20Keycloak%20Guide%20-%20HTML/file-20260217013000538.png)
![](assets/1%20-%20Keycloak%20Guide%20-%20HTML/file-20260217013013420.png)
![](assets/1%20-%20Keycloak%20Guide%20-%20HTML/file-20260217013027995.png)
![](assets/1%20-%20Keycloak%20Guide%20-%20HTML/file-20260217013044189.png)
![](assets/1%20-%20Keycloak%20Guide%20-%20HTML/file-20260217013057496.png)
![](assets/1%20-%20Keycloak%20Guide%20-%20HTML/file-20260217013108284.png)
![](assets/1%20-%20Keycloak%20Guide%20-%20HTML/file-20260217013119444.png)
![](assets/1%20-%20Keycloak%20Guide%20-%20HTML/file-20260217013134496.png)


```python
import os
import requests
from dataclasses import dataclass

# ── CONFIG ────────────────────────────────────────────
# Set these as environment variables in production.
# Never hardcode secrets in source code.
KEYCLOAK_URL    = "http://localhost:8080"
REALM           = "myrealm"
CLIENT_ID       = "my-api-client"
CLIENT_SECRET   = os.getenv("KC_CLIENT_SECRET", "Ab3xK9mP2qR7nT4vY1wS6uJ8cL0eF5gH")

# Keycloak token endpoint — always follows this pattern
TOKEN_URL = (
    f"{KEYCLOAK_URL}/realms/{REALM}"
    "/protocol/openid-connect/token"
)

# ── STEP 1: Request a token with specific scopes ──────
def get_token(requested_scopes: str) -> dict:
    """
    OAuth2 Client Credentials grant.
    requested_scopes: space-separated e.g. "ro" or "ro rw"
    Returns the full token response dict.
    """
    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type":    "client_credentials",
            "client_id":     CLIENT_ID,
            "client_secret":  CLIENT_SECRET,
            "scope":          requested_scopes,  # ← your ro/rw scopes here
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10,
    )
    response.raise_for_status()  # raises on 4xx/5xx
    return response.json()

# ── Try it ────────────────────────────────────────────
if __name__ == "__main__":
    # Request read-only token
    token_data = get_token("ro")

    print("access_token:", token_data["access_token"][:60], "...")
    print("expires_in  :", token_data["expires_in"], "seconds")
    print("token_type  :", token_data["token_type"])
    print("scope       :", token_data.get("scope"))
```
![](assets/1%20-%20Keycloak%20Guide%20-%20HTML/file-20260217013226623.png)
![](assets/1%20-%20Keycloak%20Guide%20-%20HTML/file-20260217013235774.png)


```python
import requests
from jose import jwt, JWTError, jwk
from jose.utils import base64url_decode
import json, time
from functools import lru_cache

KEYCLOAK_URL = "http://localhost:8080"
REALM        = "myrealm"
CLIENT_ID    = "my-api-client"

# Keycloak's OIDC discovery doc (has JWKS URI + issuer)
DISCOVERY_URL = (
    f"{KEYCLOAK_URL}/realms/{REALM}"
    "/.well-known/openid-configuration"
)

# ── STEP 8a: Fetch JWKS (public keys) ────────────────
# Cache so we don't hit Keycloak on every request.
# In production: add TTL-based cache refresh.
@lru_cache(maxsize=1)
def get_jwks() -> dict:
    discovery = requests.get(DISCOVERY_URL, timeout=5).json()
    jwks_uri  = discovery["jwks_uri"]
    return requests.get(jwks_uri, timeout=5).json()

@lru_cache(maxsize=1)
def get_issuer() -> str:
    discovery = requests.get(DISCOVERY_URL, timeout=5).json()
    return discovery["issuer"]

# ── STEP 8b: Validate the JWT ─────────────────────────
def validate_token(access_token: str) -> dict:
    """
    Validates the JWT:
      ✓ Signature  (using Keycloak's public key via JWKS)
      ✓ Expiry     (exp claim)
      ✓ Issuer     (must match our Keycloak realm)
      ✓ Audience   (must include our client_id)
    Returns decoded claims dict if valid.
    Raises JWTError if invalid.
    """
    jwks    = get_jwks()
    issuer  = get_issuer()

    try:
        claims = jwt.decode(
            access_token,
            jwks,                        # public key from Keycloak JWKS
            algorithms=["RS256"],        # Keycloak uses RS256 by default
            issuer=issuer,               # verifies "iss" claim
            audience=CLIENT_ID,          # verifies "aud" claim
            options={"verify_at_hash": False},
        )
    except JWTError as e:
        raise ValueError(f"Token validation failed: {e}")

    return claims  # ← Step 9: claims extracted

# ── Step 9: Read claims from the token ───────────────
def inspect_claims(claims: dict):
    print("\n── Token Claims ──────────────────────")
    print(f"  subject   : {claims.get('sub')}")
    print(f"  issuer    : {claims.get('iss')}")
    print(f"  scope     : {claims.get('scope')}")   # ← "ro rw" etc.
    print(f"  client_id : {claims.get('azp')}")
    print(f"  expires   : {claims.get('exp')}")
    print(f"  roles     : {claims.get('realm_access', {}).get('roles', [])}")
    print("──────────────────────────────────────")
```

![](assets/1%20-%20Keycloak%20Guide%20-%20HTML/file-20260217013257698.png)![](assets/1%20-%20Keycloak%20Guide%20-%20HTML/file-20260217013308387.png)

```python
from typing import List
from functools import wraps

# ── SCOPE CHECK (RBAC by scope) ───────────────────────
def has_scope(claims: dict, required: str) -> bool:
    """Check if the token contains the required scope."""
    token_scopes = claims.get("scope", "").split()
    return required in token_scopes

def require_scope(required: str):
    """Decorator: raises PermissionError if scope is missing."""
    def decorator(func):
        @wraps(func)
        def wrapper(claims: dict, *args, **kwargs):
            if not has_scope(claims, required):
                raise PermissionError(
                    f"403 Forbidden: scope '{required}' required. "
                    f"Token has: {claims.get('scope')}"
                )
            return func(claims, *args, **kwargs)
        return wrapper
    return decorator

# ── ROLE CHECK (RBAC by Keycloak realm role) ─────────
def has_role(claims: dict, required: str) -> bool:
    """
    Keycloak puts realm roles under:
      claims["realm_access"]["roles"]
    Client-specific roles are under:
      claims["resource_access"]["my-api-client"]["roles"]
    """
    realm_roles  = claims.get("realm_access", {}).get("roles", [])
    client_roles = (
        claims.get("resource_access", {})
              .get("my-api-client", {})
              .get("roles", [])
    )
    return required in realm_roles or required in client_roles

# ── SIMULATED API ENDPOINTS ───────────────────────────
@require_scope("ro")
def api_get_data(claims: dict) -> dict:
    """Requires scope: ro"""
    return {"data": ["item1", "item2"], "read_by": claims["sub"]}

@require_scope("rw")
def api_write_data(claims: dict, payload: dict) -> dict:
    """Requires scope: rw"""
    return {"written": payload, "by": claims["sub"]}

def api_admin_action(claims: dict) -> dict:
    """Requires role: admin"""
    if not has_role(claims, "admin"):
        raise PermissionError("403 Forbidden: role 'admin' required")
    return {"admin_data": "secret stuff", "by": claims["sub"]}
```

![](assets/1%20-%20Keycloak%20Guide%20-%20HTML/file-20260217013338521.png)

```python
import os, sys, requests, json
from jose import jwt, JWTError
from functools import lru_cache, wraps

# ═══════════════════════════════════════════════════
#  CONFIG — edit these to match your Keycloak setup
# ═══════════════════════════════════════════════════
KEYCLOAK_URL  = "http://localhost:8080"
REALM         = "myrealm"
CLIENT_ID     = "my-api-client"
CLIENT_SECRET = os.getenv("KC_CLIENT_SECRET", "PASTE-YOUR-SECRET-HERE")

TOKEN_URL  = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"
DISCO_URL  = f"{KEYCLOAK_URL}/realms/{REALM}/.well-known/openid-configuration"

# ═══════════════════════════════════════════════════
#  AUTH: Get token from Keycloak
# ═══════════════════════════════════════════════════
def get_token(scopes: str) -> str:
    r = requests.post(TOKEN_URL, data={
        "grant_type":   "client_credentials",
        "client_id":    CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope":        scopes,
    }, timeout=10)
    r.raise_for_status()
    return r.json()["access_token"]

# ═══════════════════════════════════════════════════
#  VALIDATE: Verify JWT using Keycloak's public key
# ═══════════════════════════════════════════════════
@lru_cache(maxsize=1)
def _get_keycloak_public_keys():
    disco  = requests.get(DISCO_URL, timeout=5).json()
    return requests.get(disco["jwks_uri"], timeout=5).json()

def validate_and_decode(token: str) -> dict:
    jwks   = _get_keycloak_public_keys()
    issuer = f"{KEYCLOAK_URL}/realms/{REALM}"
    return jwt.decode(
        token, jwks,
        algorithms=["RS256"],
        issuer=issuer,
        audience=CLIENT_ID,
        options={"verify_at_hash": False},
    )

# ═══════════════════════════════════════════════════
#  AUTHORIZE: Scope and role enforcement
# ═══════════════════════════════════════════════════
def require_scope(scope: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(claims, *a, **kw):
            if scope not in claims.get("scope", "").split():
                raise PermissionError(f"❌ 403: requires scope '{scope}'")
            return fn(claims, *a, **kw)
        return wrapper
    return decorator

def require_role(role: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(claims, *a, **kw):
            roles = claims.get("realm_access", {}).get("roles", [])
            if role not in roles:
                raise PermissionError(f"❌ 403: requires role '{role}'")
            return fn(claims, *a, **kw)
        return wrapper
    return decorator

# ═══════════════════════════════════════════════════
#  SIMULATED API ENDPOINTS
# ═══════════════════════════════════════════════════
@require_scope("ro")
def api_read(claims):
    return f"✅ GET /data  — read by {claims['azp']}"

@require_scope("rw")
def api_write(claims):
    return f"✅ POST /data — written by {claims['azp']}"

@require_role("admin")
def api_admin(claims):
    return f"✅ GET /admin — accessed by {claims['azp']}"

def try_call(label, fn, claims):
    print(f"\n  Calling {label}")
    try:
        result = fn(claims)
        print(f"  {result}")
    except PermissionError as e:
        print(f"  {e}")
    except JWTError as e:
        print(f"  ❌ JWT Error: {e}")

# ═══════════════════════════════════════════════════
#  RUN THE DEMO
# ═══════════════════════════════════════════════════
if __name__ == "__main__":
    print("\n🔐 Keycloak OAuth2 Demo\n" + "="*40)

    # ── Test 1: ro-only token ──────────────────────
    print("\n[1] Token with scope 'ro'")
    ro_token  = get_token("ro")
    ro_claims = validate_and_decode(ro_token)
    print(f"  scope in token: {ro_claims.get('scope')}")
    try_call("api_read  (needs ro)", api_read,  ro_claims)
    try_call("api_write (needs rw)", api_write, ro_claims)

    # ── Test 2: rw token ───────────────────────────
    print("\n[2] Token with scope 'ro rw'")
    rw_token  = get_token("ro rw")
    rw_claims = validate_and_decode(rw_token)
    print(f"  scope in token: {rw_claims.get('scope')}")
    try_call("api_read  (needs ro)", api_read,  rw_claims)
    try_call("api_write (needs rw)", api_write, rw_claims)
    try_call("api_admin (needs role admin)", api_admin, rw_claims)

    print("\n✅ Demo complete")
```

![](assets/1%20-%20Keycloak%20Guide%20-%20HTML/file-20260217013406221.png)![](assets/1%20-%20Keycloak%20Guide%20-%20HTML/file-20260217013419709.png)
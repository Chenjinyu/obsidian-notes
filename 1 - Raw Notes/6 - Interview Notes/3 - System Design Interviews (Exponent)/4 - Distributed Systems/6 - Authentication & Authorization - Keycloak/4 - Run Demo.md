```python
"""
run_demo.py
===========
Complete end-to-end demo: Authenticate with Keycloak → Validate JWT → Enforce AuthZ.

This is the single file that ties everything together.
Run it after starting Keycloak (see guide) and setting your client secret.

    export KC_CLIENT_SECRET="your-secret-from-keycloak"
    pip install requests python-jose[cryptography]
    python run_demo.py
"""

import os
import sys
import requests
from functools import lru_cache, wraps
from jose import jwt, JWTError

# ─── CONFIG ───────────────────────────────────────────────────────────────────

KEYCLOAK_URL  = os.getenv("KC_URL",           "http://localhost:8080")
REALM         = os.getenv("KC_REALM",         "myrealm")
CLIENT_ID     = os.getenv("KC_CLIENT_ID",     "my-api-client")
CLIENT_SECRET = os.getenv("KC_CLIENT_SECRET", "PASTE-YOUR-SECRET-HERE")

TOKEN_URL     = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"
DISCO_URL     = f"{KEYCLOAK_URL}/realms/{REALM}/.well-known/openid-configuration"
ISSUER        = f"{KEYCLOAK_URL}/realms/{REALM}"

# ══════════════════════════════════════════════════════════════════════════════
#  AUTHENTICATION — Step 1-6
#  Client sends client_id + client_secret → Keycloak returns JWT
# ══════════════════════════════════════════════════════════════════════════════

def get_token(scopes: str) -> str:
    """
    OAuth2 Client Credentials grant.
    Sends client_id + client_secret to Keycloak, requests specific scopes.
    Returns the raw access_token JWT string.
    """
    r = requests.post(
        TOKEN_URL,
        data={
            "grant_type":    "client_credentials",
            "client_id":     CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope":         scopes,          # "ro" | "ro rw" | etc.
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["access_token"]


# ══════════════════════════════════════════════════════════════════════════════
#  TOKEN VALIDATION — Step 7-9
#  Resource server verifies JWT using Keycloak's public key (no secret needed)
# ══════════════════════════════════════════════════════════════════════════════

@lru_cache(maxsize=1)
def _get_jwks() -> dict:
    """Fetch and cache Keycloak's public signing keys (JWKS)."""
    disco = requests.get(DISCO_URL, timeout=5).json()
    return requests.get(disco["jwks_uri"], timeout=5).json()


def validate_token(access_token: str) -> dict:
    """
    Step 8: Validates the JWT:
      ✓ Signature  (RSA public key from Keycloak JWKS — no secret sharing needed)
      ✓ Expiry     (exp claim)
      ✓ Issuer     (iss must match our realm)
      ✓ Audience   (aud must include our client_id)

    Step 9: Returns decoded claims dict.
    Raises JWTError on any validation failure.
    """
    try:
        return jwt.decode(
            access_token,
            _get_jwks(),                   # Keycloak's RSA public key
            algorithms=["RS256"],
            issuer=ISSUER,
            audience=CLIENT_ID,
            options={"verify_at_hash": False},
        )
    except JWTError as e:
        raise JWTError(f"Token invalid: {e}")


# ══════════════════════════════════════════════════════════════════════════════
#  AUTHORIZATION — Step 10
#  Enforce scopes (OAuth2) and roles (RBAC) extracted from claims
# ══════════════════════════════════════════════════════════════════════════════

# ── Scope check ───────────────────────────────────────────────────────────────

def has_scope(claims: dict, scope: str) -> bool:
    """True if the scope claim contains the required scope."""
    return scope in claims.get("scope", "").split()


def require_scope(scope: str):
    """
    Decorator for API endpoint functions.
    First argument of the decorated function must be `claims` dict.

    Usage:
        @require_scope("rw")
        def api_write(claims, payload):
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(claims, *args, **kwargs):
            if not has_scope(claims, scope):
                token_scopes = claims.get("scope", "none")
                raise PermissionError(
                    f"403 Forbidden — requires scope '{scope}'. "
                    f"Token has: '{token_scopes}'"
                )
            return fn(claims, *args, **kwargs)
        return wrapper
    return decorator


# ── Role check ────────────────────────────────────────────────────────────────

def has_role(claims: dict, role: str) -> bool:
    """
    Check for a role in either realm-level or client-level roles.

    Keycloak stores roles in two places in the JWT:
      • realm_access.roles       → roles valid across all clients in the realm
      • resource_access.<id>.roles → roles specific to this client
    """
    realm_roles = claims.get("realm_access", {}).get("roles", [])
    client_roles = (
        claims.get("resource_access", {})
              .get(CLIENT_ID, {})
              .get("roles", [])
    )
    return role in realm_roles or role in client_roles


def require_role(role: str):
    """Decorator: raises PermissionError if role is not in token claims."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(claims, *args, **kwargs):
            if not has_role(claims, role):
                raise PermissionError(
                    f"403 Forbidden — requires role '{role}'"
                )
            return fn(claims, *args, **kwargs)
        return wrapper
    return decorator


# ── ABAC helper (attribute-based) ─────────────────────────────────────────────

def abac_check(claims: dict, required_group: str, resource_tag: str) -> bool:
    """
    Simple ABAC policy:
      user must be in required_group AND resource must match tag.
    In production: replace this with OPA (Open Policy Agent) calls.
    """
    groups = claims.get("groups", [])          # Keycloak group mapper needed
    return required_group in groups


# ══════════════════════════════════════════════════════════════════════════════
#  SIMULATED API ENDPOINTS
# ══════════════════════════════════════════════════════════════════════════════

@require_scope("ro")
def api_read_data(claims: dict) -> str:
    """GET /data — requires scope: ro"""
    return f"[GET /data] Data returned to client '{claims.get('azp')}'"


@require_scope("rw")
def api_write_data(claims: dict, payload: dict) -> str:
    """POST /data — requires scope: rw"""
    return f"[POST /data] Saved {payload} by client '{claims.get('azp')}'"


@require_scope("rw")
@require_role("data-manager")
def api_delete_data(claims: dict) -> str:
    """DELETE /data — requires scope: rw AND role: data-manager"""
    return f"[DELETE /data] Deleted by '{claims.get('azp')}'"


@require_role("admin")
def api_admin_panel(claims: dict) -> str:
    """GET /admin — requires realm role: admin"""
    return f"[GET /admin] Admin panel accessed by '{claims.get('azp')}'"


# ══════════════════════════════════════════════════════════════════════════════
#  RUN THE DEMO
# ══════════════════════════════════════════════════════════════════════════════

def section(title: str):
    print(f"\n{'─'*52}")
    print(f"  {title}")
    print(f"{'─'*52}")

def try_endpoint(label: str, fn, claims, *args):
    """Call an endpoint and print pass/fail result."""
    try:
        result = fn(claims, *args)
        print(f"  ✅ {result}")
    except PermissionError as e:
        print(f"  ❌ {e}")
    except JWTError as e:
        print(f"  ❌ JWT error: {e}")


if __name__ == "__main__":
    print("\n🔐 Keycloak OAuth2 + OIDC Full Demo")
    print("=" * 52)

    # ── Check Keycloak is reachable ───────────────────────
    print("\n[0] Checking Keycloak connection...")
    try:
        disco = requests.get(DISCO_URL, timeout=5).json()
        print(f"  ✅ Connected. Issuer: {disco['issuer']}")
    except Exception as e:
        print(f"  ❌ Cannot reach Keycloak at {KEYCLOAK_URL}: {e}")
        print("\n  Make sure Keycloak is running:")
        print("  docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin \\")
        print("    -e KEYCLOAK_ADMIN_PASSWORD=admin \\")
        print("    quay.io/keycloak/keycloak:24.0 start-dev")
        sys.exit(1)

    # ────────────────────────────────────────────────────────
    section("TEST 1: Token with scope 'ro' only")
    # ────────────────────────────────────────────────────────

    print("\n  [AuthN] Requesting token with scope='ro'...")
    try:
        ro_token = get_token("ro")
        print(f"  Token received (first 60 chars): {ro_token[:60]}...")
    except requests.HTTPError as e:
        print(f"  ❌ Auth failed: {e.response.text[:300]}")
        sys.exit(1)

    print("\n  [Validate] Verifying JWT signature + claims...")
    ro_claims = validate_token(ro_token)
    print(f"  ✅ Token valid")
    print(f"     sub    : {ro_claims.get('sub')}")
    print(f"     azp    : {ro_claims.get('azp')}  (authorized party = client_id)")
    print(f"     scope  : {ro_claims.get('scope')}")
    print(f"     exp    : {ro_claims.get('exp')}")

    print("\n  [AuthZ] Calling API endpoints with ro token...")
    try_endpoint("api_read_data  (needs ro)", api_read_data, ro_claims)
    try_endpoint("api_write_data (needs rw)", api_write_data, ro_claims, {"key": "value"})
    try_endpoint("api_admin_panel(needs admin role)", api_admin_panel, ro_claims)

    # ────────────────────────────────────────────────────────
    section("TEST 2: Token with scope 'ro rw'")
    # ────────────────────────────────────────────────────────

    print("\n  [AuthN] Requesting token with scope='ro rw'...")
    try:
        rw_token  = get_token("ro rw")
        rw_claims = validate_token(rw_token)
        print(f"  ✅ Token valid — scope: {rw_claims.get('scope')}")
    except requests.HTTPError as e:
        print(f"  ❌ Auth failed: {e.response.text[:300]}")
        sys.exit(1)

    print("\n  [AuthZ] Calling API endpoints with ro rw token...")
    try_endpoint("api_read_data  (needs ro)", api_read_data, rw_claims)
    try_endpoint("api_write_data (needs rw)", api_write_data, rw_claims, {"item": "new"})
    try_endpoint("api_delete_data(needs rw + role data-manager)", api_delete_data, rw_claims)
    try_endpoint("api_admin_panel(needs role admin)", api_admin_panel, rw_claims)

    # ────────────────────────────────────────────────────────
    section("TEST 3: Security — tampered token")
    # ────────────────────────────────────────────────────────

    print("\n  [Security] Testing tampered token rejection...")
    bad_token = ro_token[:-15] + "AAAABBBBCCCC000"
    try:
        validate_token(bad_token)
        print("  ⚠  Should NOT reach here — tampered token accepted!")
    except JWTError as e:
        print(f"  ✅ Tampered token correctly rejected")

    # ────────────────────────────────────────────────────────
    section("Summary")
    # ────────────────────────────────────────────────────────

    print("""
  Flow completed:
  
  1. CLIENT sends client_id + client_secret + requested scope
     to Keycloak token endpoint (OAuth2 client_credentials grant)
  
  2. KEYCLOAK verifies credentials, checks client is allowed
     the requested scopes, then issues a signed JWT (RS256)
  
  3. CLIENT sends request to your API with:
     Authorization: Bearer <access_token>
  
  4. YOUR API (resource server) validates the JWT using
     Keycloak's public key (fetched from JWKS endpoint)
     — no call to Keycloak needed per request
  
  5. YOUR API extracts claims and checks:
     • scope claim  → for OAuth2 scope enforcement (ro/rw)
     • realm_access.roles → for RBAC role enforcement (admin)
  
  6. Allow or Deny the request
    """)

    print("✅ Demo complete\n")
```
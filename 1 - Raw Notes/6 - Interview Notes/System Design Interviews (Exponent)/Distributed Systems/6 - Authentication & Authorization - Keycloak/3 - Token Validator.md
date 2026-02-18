```python
"""
keycloak_auth.py
================
Step 1-6: Authenticate against Keycloak and get JWT tokens.

Usage:
    export KC_CLIENT_SECRET="your-secret-from-keycloak"
    python keycloak_auth.py
"""

import os
import requests
from functools import lru_cache

# ─── CONFIG ──────────────────────────────────────────────────────────────────
# Set these via environment variables in production. Never hardcode secrets.

KEYCLOAK_URL  = os.getenv("KC_URL",    "http://localhost:8080")
REALM         = os.getenv("KC_REALM",  "myrealm")
CLIENT_ID     = os.getenv("KC_CLIENT_ID",     "my-api-client")
CLIENT_SECRET = os.getenv("KC_CLIENT_SECRET", "PASTE-YOUR-SECRET-HERE")

# Keycloak's token endpoint always follows this URL pattern
TOKEN_URL = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"

# ─── STEP 1-2: Get token (Client Credentials flow) ───────────────────────────

def get_token(scopes: str = "ro") -> dict:
    """
    OAuth2 Client Credentials grant — server-to-server authentication.

    Args:
        scopes: space-separated scope string e.g. "ro" or "ro rw"

    Returns:
        Full token response dict with keys:
          - access_token  (JWT — send this in Authorization header)
          - expires_in    (seconds until token expires)
          - token_type    (always "Bearer")
          - scope         (scopes actually granted by Keycloak)

    Raises:
        requests.HTTPError if Keycloak rejects the request (wrong secret,
        unknown scope, client not allowed scope, etc.)
    """
    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type":    "client_credentials",
            "client_id":     CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope":         scopes,       # ← request specific scopes here
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10,
    )

    # Keycloak returns 401 for bad secret, 400 for unknown scope
    response.raise_for_status()
    return response.json()


def get_access_token(scopes: str = "ro") -> str:
    """Convenience wrapper — returns just the access_token string."""
    return get_token(scopes)["access_token"]


# ─── DISCOVERY: OIDC metadata ─────────────────────────────────────────────────

@lru_cache(maxsize=1)
def get_discovery() -> dict:
    """
    Fetch Keycloak's OIDC discovery document.
    Contains: issuer, token_endpoint, jwks_uri, scopes_supported, etc.
    Cached — Keycloak's discovery doc rarely changes.
    """
    url = f"{KEYCLOAK_URL}/realms/{REALM}/.well-known/openid-configuration"
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    return r.json()


# ─── MAIN (demo) ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  Keycloak Authentication Demo")
    print("=" * 55)

    # ── Show discovery metadata
    print("\n[0] OIDC Discovery metadata:")
    disco = get_discovery()
    print(f"  issuer       : {disco['issuer']}")
    print(f"  token_url    : {disco['token_endpoint']}")
    print(f"  jwks_uri     : {disco['jwks_uri']}")

    # ── Get a read-only token
    print("\n[1] Requesting token with scope='ro':")
    try:
        data = get_token("ro")
        print(f"  access_token : {data['access_token'][:50]}...")
        print(f"  expires_in   : {data['expires_in']} seconds")
        print(f"  token_type   : {data['token_type']}")
        print(f"  scope        : {data.get('scope')}")
    except requests.HTTPError as e:
        print(f"  ERROR: {e.response.status_code} — {e.response.text[:200]}")

    # ── Get a read-write token
    print("\n[2] Requesting token with scope='ro rw':")
    try:
        data = get_token("ro rw")
        print(f"  scope granted: {data.get('scope')}")
    except requests.HTTPError as e:
        print(f"  ERROR: {e.response.status_code} — {e.response.text[:200]}")

    # ── Try requesting a scope not assigned to this client
    print("\n[3] Requesting scope 'admin' (not assigned to client — expect error):")
    try:
        data = get_token("admin")
        print(f"  scope granted: {data.get('scope')}")
    except requests.HTTPError as e:
        print(f"  Expected 400/403: {e.response.status_code}")
```
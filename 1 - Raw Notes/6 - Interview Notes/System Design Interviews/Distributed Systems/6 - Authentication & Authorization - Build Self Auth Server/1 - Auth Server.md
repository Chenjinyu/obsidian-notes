```python

"""
auth_server.py
==============
Step 1-6: AuthN + AuthZ token issuance server.

Handles:
  - Client registration (generates client_id + client_secret)
  - Scope definition (rw, ro)
  - OAuth2 Client Credentials flow (server-to-server)
  - User login flow (username + password)
  - JWT access_token + id_token + refresh_token issuance
  - RBAC role claims embedded in token
"""

import uuid
import hashlib
import hmac
import secrets
import time
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from jose import jwt, JWTError

# ─── CONFIG ──────────────────────────────────────────────────────────────────

SECRET_KEY = "super-secret-key-change-in-production-use-rsa-in-real-world"
ALGORITHM = "HS256"
ISSUER = "http://localhost:8000"  # auth server URL
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
ID_TOKEN_EXPIRE_MINUTES = 15

# ─── MOCK DATABASES ──────────────────────────────────────────────────────────

# Defined scopes: scope_name -> description
SCOPES_DB = {
    "rw": "Read and Write access to resources",
    "ro": "Read-Only access to resources",
    "admin": "Full administrative access",
}

# Registered OAuth2 clients (server-to-server)
# In production: store in DB, hash the secret
CLIENTS_DB = {
    # client_id -> { client_secret, allowed_scopes, roles }
    "service-client-001": {
        "client_secret": "my-super-secret-value",
        "allowed_scopes": ["ro", "rw"],
        "roles": ["service_reader", "service_writer"],
    }
}

# Human users (app user flow)
# password is hashed with sha256 for demo — use bcrypt in production
def _hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

USERS_DB = {
    "alice": {
        "password_hash": _hash_pw("password123"),
        "roles": ["admin"],
        "groups": ["engineering", "admin-group"],
        "email": "alice@example.com",
        "allowed_scopes": ["ro", "rw", "admin"],
    },
    "bob": {
        "password_hash": _hash_pw("bobpass"),
        "roles": ["viewer"],
        "groups": ["read-only-group"],
        "email": "bob@example.com",
        "allowed_scopes": ["ro"],
    },
}

# ACL: resource_id -> { user/client -> permissions }
ACL_DB = {
    "resource:reports": {
        "alice": ["read", "write", "delete"],
        "bob": ["read"],
        "service-client-001": ["read", "write"],
    },
    "resource:admin-panel": {
        "alice": ["read", "write", "delete"],
    }
}

# Refresh token store: refresh_token -> payload
REFRESH_TOKEN_STORE = {}

# ─── APP ─────────────────────────────────────────────────────────────────────

app = FastAPI(title="Auth Server", description="AuthN + AuthZ token issuer")
security = HTTPBasic()

# ─── MODELS ──────────────────────────────────────────────────────────────────

class RegisterClientRequest(BaseModel):
    client_name: str
    allowed_scopes: list[str]
    roles: list[str] = []

class ClientCredentialsRequest(BaseModel):
    """Server-to-server: OAuth2 client_credentials grant"""
    client_id: str
    client_secret: str
    scope: str  # space-separated e.g. "ro rw"
    grant_type: str = "client_credentials"

class UserLoginRequest(BaseModel):
    """Human user login"""
    username: str
    password: str
    scope: str = "ro"

class RefreshTokenRequest(BaseModel):
    refresh_token: str
    grant_type: str = "refresh_token"

# ─── TOKEN HELPERS ───────────────────────────────────────────────────────────

def _create_access_token(subject: str, scopes: list, roles: list, extra_claims: dict = {}) -> str:
    """Step 5-6: Build JWT access_token with claims"""
    now = datetime.now(timezone.utc)
    payload = {
        "iss": ISSUER,                   # issuer
        "sub": subject,                  # subject (user or client_id)
        "iat": int(now.timestamp()),     # issued at
        "exp": int((now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()),
        "jti": str(uuid.uuid4()),        # unique token ID (for revocation)
        "scope": " ".join(scopes),       # granted scopes
        "roles": roles,                  # RBAC roles
        **extra_claims
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def _create_id_token(subject: str, email: str, groups: list) -> str:
    """OIDC id_token — carries identity (who you are)"""
    now = datetime.now(timezone.utc)
    payload = {
        "iss": ISSUER,
        "sub": subject,
        "aud": ISSUER,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ID_TOKEN_EXPIRE_MINUTES)).timestamp()),
        "email": email,
        "groups": groups,               # AD groups / IdP groups
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def _create_refresh_token(subject: str, scopes: list) -> str:
    """Opaque refresh token stored server-side"""
    token = secrets.token_urlsafe(48)
    REFRESH_TOKEN_STORE[token] = {
        "sub": subject,
        "scopes": scopes,
        "exp": time.time() + (REFRESH_TOKEN_EXPIRE_DAYS * 86400)
    }
    return token

# ─── ENDPOINTS ───────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Auth Server running", "scopes_available": SCOPES_DB}


# ── Step 0: Admin registers a new client ─────────────────────────────────────
@app.post("/admin/register-client")
def register_client(req: RegisterClientRequest):
    """
    Admin endpoint to create a new OAuth2 client (client_id + client_secret).
    In production: protect with admin token.
    """
    # Validate requested scopes exist
    for s in req.allowed_scopes:
        if s not in SCOPES_DB:
            raise HTTPException(400, f"Unknown scope '{s}'. Available: {list(SCOPES_DB.keys())}")

    client_id = f"client-{secrets.token_hex(8)}"
    client_secret = secrets.token_urlsafe(32)

    CLIENTS_DB[client_id] = {
        "client_secret": client_secret,
        "allowed_scopes": req.allowed_scopes,
        "roles": req.roles,
    }

    return {
        "message": "Client registered successfully",
        "client_id": client_id,
        "client_secret": client_secret,  # Show ONCE — store securely!
        "allowed_scopes": req.allowed_scopes,
        "note": "Store the client_secret securely. It will not be shown again."
    }


# ── Step 1-6: Server-to-Server token (client_credentials grant) ──────────────
@app.post("/token/client-credentials")
def client_credentials_token(req: ClientCredentialsRequest):
    """
    OAuth2 client_credentials flow.
    Step 1: Client sends client_id + client_secret
    Step 2: Server verifies credentials against CLIENTS_DB
    Step 5-6: Server issues access_token with scopes + roles
    """
    # Step 2: Verify client identity
    client = CLIENTS_DB.get(req.client_id)
    if not client:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid client_id")

    # Constant-time compare to prevent timing attacks
    if not hmac.compare_digest(client["client_secret"], req.client_secret):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid client_secret")

    # Validate requested scopes
    requested_scopes = req.scope.split()
    for s in requested_scopes:
        if s not in SCOPES_DB:
            raise HTTPException(400, f"Unknown scope: {s}")
        if s not in client["allowed_scopes"]:
            raise HTTPException(403, f"Client not allowed scope: {s}")

    # Step 5-6: Issue token
    access_token = _create_access_token(
        subject=req.client_id,
        scopes=requested_scopes,
        roles=client["roles"],
        extra_claims={"client_id": req.client_id, "token_type_hint": "service"}
    )

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "scope": req.scope,
    }


# ── Step 1-6: Human user login ────────────────────────────────────────────────
@app.post("/token/login")
def user_login(req: UserLoginRequest):
    """
    Human user login flow.
    Step 1: Client sends username + password
    Step 2: Server verifies against USERS_DB (simulates IdP check)
    Step 4: Fetch user attributes/groups from IdP (simulated)
    Step 5-6: Issue access_token + id_token + refresh_token
    """
    # Step 2: Verify user identity (simulate IdP check)
    user = USERS_DB.get(req.username)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    if not hmac.compare_digest(user["password_hash"], _hash_pw(req.password)):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    # Validate scopes
    requested_scopes = req.scope.split()
    for s in requested_scopes:
        if s not in SCOPES_DB:
            raise HTTPException(400, f"Unknown scope: {s}")
        if s not in user["allowed_scopes"]:
            raise HTTPException(403, f"User not permitted scope: {s}")

    # Step 4: Fetch user attributes/groups from IdP (mocked)
    # In real world: LDAP query to AD, or call to Okta /userinfo
    groups = user["groups"]
    roles = user["roles"]

    # Step 5-6: Issue tokens
    access_token = _create_access_token(
        subject=req.username,
        scopes=requested_scopes,
        roles=roles,
        extra_claims={"email": user["email"], "groups": groups}
    )
    id_token = _create_id_token(req.username, user["email"], groups)
    refresh_token = _create_refresh_token(req.username, requested_scopes)

    return {
        "access_token": access_token,   # use for API calls
        "id_token": id_token,           # OIDC: who you are
        "refresh_token": refresh_token, # use to get new access_token
        "token_type": "Bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "scope": req.scope,
    }


# ── Refresh token exchange ────────────────────────────────────────────────────
@app.post("/token/refresh")
def refresh_token(req: RefreshTokenRequest):
    """Exchange refresh_token for a new access_token without re-login"""
    stored = REFRESH_TOKEN_STORE.get(req.refresh_token)
    if not stored:
        raise HTTPException(401, "Invalid or expired refresh token")
    if time.time() > stored["exp"]:
        del REFRESH_TOKEN_STORE[req.refresh_token]
        raise HTTPException(401, "Refresh token expired")

    subject = stored["sub"]
    scopes = stored["scopes"]

    # Re-fetch latest roles/groups from IdP (important: roles may have changed)
    user = USERS_DB.get(subject)
    roles = user["roles"] if user else []
    groups = user["groups"] if user else []

    access_token = _create_access_token(
        subject=subject,
        scopes=scopes,
        roles=roles,
        extra_claims={"email": user.get("email", ""), "groups": groups} if user else {}
    )

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "scope": " ".join(scopes),
    }


# ── JWKS endpoint (public keys for token verification) ───────────────────────
@app.get("/.well-known/jwks.json")
def jwks():
    """
    In production with RS256: expose public key here so resource servers
    can verify tokens WITHOUT calling auth server (zero-trust token validation).
    With HS256 (symmetric), resource servers share the secret instead.
    """
    return {"keys": [], "note": "Use RS256 + real JWKS in production"}


# ── Scope discovery ───────────────────────────────────────────────────────────
@app.get("/scopes")
def list_scopes():
    return {"scopes": SCOPES_DB}


# ── ACL lookup (used by resource server) ─────────────────────────────────────
@app.get("/acl/{resource_id}/{subject}")
def get_acl(resource_id: str, subject: str):
    resource_acl = ACL_DB.get(resource_id, {})
    permissions = resource_acl.get(subject, [])
    return {"resource": resource_id, "subject": subject, "permissions": permissions}
```
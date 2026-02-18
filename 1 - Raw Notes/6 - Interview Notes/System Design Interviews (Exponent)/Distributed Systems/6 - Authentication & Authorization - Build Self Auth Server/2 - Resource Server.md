## Steps Diagram
 - [[../6 - Authentication & Authorization -  Deep Dive|6 - Authentication & Authorization -  Deep Dive]]
 
```python
"""
resource_server.py
==================
Step 7-10: Your actual REST API (Resource Server).

Handles:
  - Step 7: Receives Bearer token in Authorization header
  - Step 8: Validates JWT (signature, expiry, issuer)
  - Step 9: Extracts claims (roles, scopes, groups)
  - Step 10: Applies RBAC, ABAC, and ACL authorization
"""

from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import httpx

# ─── CONFIG ──────────────────────────────────────────────────────────────────

SECRET_KEY = "super-secret-key-change-in-production-use-rsa-in-real-world"
ALGORITHM = "HS256"
EXPECTED_ISSUER = "http://localhost:8000"
AUTH_SERVER_URL = "http://localhost:8000"

# ─── APP ─────────────────────────────────────────────────────────────────────

app = FastAPI(title="Resource Server (Your API)", description="Protected API endpoints")
bearer_scheme = HTTPBearer()

# ─── TOKEN VALIDATION ────────────────────────────────────────────────────────

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    """
    Step 8: Validate JWT token.
    - Verify signature (no network call needed with shared secret or JWKS)
    - Check expiry
    - Check issuer
    Returns decoded claims dict.
    """
    token = credentials.credentials
    try:
        claims = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_aud": False}  # set audience in production
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify issuer
    if claims.get("iss") != EXPECTED_ISSUER:
        raise HTTPException(401, "Token issuer mismatch")

    return claims  # Step 9: claims now available to all route handlers

# ─── AUTHZ HELPERS ───────────────────────────────────────────────────────────

def require_scope(required_scope: str):
    """Step 10 RBAC/Scope check: token must have the required scope"""
    def checker(claims: dict = Depends(validate_token)):
        token_scopes = claims.get("scope", "").split()
        if required_scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required scope '{required_scope}' not in token. Token has: {token_scopes}"
            )
        return claims
    return checker

def require_role(required_role: str):
    """Step 10 RBAC check: token must have the required role"""
    def checker(claims: dict = Depends(validate_token)):
        token_roles = claims.get("roles", [])
        if required_role not in token_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role '{required_role}' not present. Token has: {token_roles}"
            )
        return claims
    return checker

def abac_check(claims: dict, resource_classification: str, required_group: str, time_restricted: bool = False) -> bool:
    """
    Step 10 ABAC check.
    Policy example: user must be in required_group AND resource must match classification.
    In production: use OPA (Open Policy Agent) for complex ABAC rules.
    """
    import datetime
    user_groups = claims.get("groups", [])

    # Attribute 1: group membership
    if required_group not in user_groups:
        return False

    # Attribute 2: time restriction (business hours 9-17)
    if time_restricted:
        hour = datetime.datetime.now().hour
        if not (9 <= hour < 17):
            return False

    return True

async def acl_check(subject: str, resource_id: str, required_permission: str) -> bool:
    """
    Step 10 ACL check.
    Calls auth server to get ACL permissions for this subject on this resource.
    In production: cache this, or embed ACL in the token itself for simple cases.
    """
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{AUTH_SERVER_URL}/acl/{resource_id}/{subject}")
            if resp.status_code == 200:
                data = resp.json()
                return required_permission in data.get("permissions", [])
        except Exception:
            pass
    return False

# ─── PROTECTED ENDPOINTS ─────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Resource Server running. All /api/* endpoints require Bearer token."}


# ── Endpoint 1: Read-only access (scope: ro) ─────────────────────────────────
@app.get("/api/data")
def get_data(claims: dict = Depends(require_scope("ro"))):
    """
    Step 7-10 in action:
    7. Client sends: Authorization: Bearer <token>
    8. Token validated (signature + expiry)
    9. Claims extracted
    10. RBAC scope check: must have 'ro' scope
    """
    return {
        "message": "Here is your read-only data",
        "requested_by": claims["sub"],
        "your_roles": claims.get("roles"),
        "your_scopes": claims.get("scope"),
    }


# ── Endpoint 2: Write access (scope: rw) ─────────────────────────────────────
@app.post("/api/data")
def write_data(payload: dict, claims: dict = Depends(require_scope("rw"))):
    """Requires 'rw' scope — read-only tokens will be rejected"""
    return {
        "message": "Data written successfully",
        "written_by": claims["sub"],
        "payload_received": payload,
    }


# ── Endpoint 3: Admin only (role check - RBAC) ────────────────────────────────
@app.get("/api/admin")
def admin_panel(claims: dict = Depends(require_role("admin"))):
    """
    Step 10 RBAC: Checks 'admin' role in token claims.
    service-client-001 and bob will be DENIED (no admin role).
    alice will be ALLOWED.
    """
    return {
        "message": "Welcome to the admin panel",
        "admin": claims["sub"],
        "groups": claims.get("groups", []),
    }


# ── Endpoint 4: ABAC policy check ─────────────────────────────────────────────
@app.get("/api/finance-report")
def finance_report(claims: dict = Depends(validate_token)):
    """
    Step 10 ABAC: Access allowed only if:
      - user is in 'engineering' or 'admin-group'
      - resource is classified as 'financial'
      - (optionally) request is during business hours
    """
    if not abac_check(claims, resource_classification="financial", required_group="admin-group"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ABAC policy denied: you must be in 'admin-group' to access financial reports"
        )
    return {
        "message": "Finance report data",
        "accessed_by": claims["sub"],
    }


# ── Endpoint 5: ACL check ─────────────────────────────────────────────────────
@app.get("/api/reports")
async def get_reports(claims: dict = Depends(validate_token)):
    """
    Step 10 ACL: Checks if this specific user has 'read' permission
    on the 'resource:reports' ACL entry.
    Each resource has its own permission list.
    """
    subject = claims["sub"]
    allowed = await acl_check(subject, "resource:reports", "read")

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"ACL denied: '{subject}' does not have 'read' permission on resource:reports"
        )

    return {
        "message": "Reports data",
        "accessed_by": subject,
        "note": "Access granted via ACL check"
    }


# ── Endpoint 6: Inspect your token claims (debugging) ────────────────────────
@app.get("/api/me")
def me(claims: dict = Depends(validate_token)):
    """Shows all claims inside your token — useful for debugging"""
    return {
        "subject": claims.get("sub"),
        "issuer": claims.get("iss"),
        "scopes": claims.get("scope"),
        "roles": claims.get("roles"),
        "groups": claims.get("groups"),
        "email": claims.get("email"),
        "expires_at": claims.get("exp"),
        "issued_at": claims.get("iat"),
        "token_id": claims.get("jti"),
    }
```
```python
"""
demo_client.py
==============
Demonstrates the FULL flow from client to auth server to resource server.

Run this AFTER starting both servers:
    uvicorn auth_server:app --port 8000 &
    uvicorn resource_server:app --port 8001

Then run: python demo_client.py
"""

import httpx
import json
import sys

AUTH_SERVER = "http://localhost:8000"
RESOURCE_SERVER = "http://localhost:8001"

def print_section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def print_result(label: str, resp: httpx.Response):
    status_icon = "✅" if resp.status_code < 400 else "❌"
    print(f"\n{status_icon} [{resp.status_code}] {label}")
    try:
        data = resp.json()
        # Truncate long tokens for readability
        if "access_token" in data:
            data["access_token"] = data["access_token"][:40] + "...[truncated]"
        if "id_token" in data:
            data["id_token"] = data["id_token"][:40] + "...[truncated]"
        print(json.dumps(data, indent=2))
    except Exception:
        print(resp.text)

# ─────────────────────────────────────────────────────────────────────────────

def demo():
    with httpx.Client(timeout=10) as client:

        # ── STEP 0: Register a new client ────────────────────────────────────
        print_section("STEP 0: Register a new OAuth2 client (admin action)")
        resp = client.post(f"{AUTH_SERVER}/admin/register-client", json={
            "client_name": "my-new-service",
            "allowed_scopes": ["ro"],
            "roles": ["service_reader"]
        })
        print_result("Register new client", resp)
        new_client = resp.json()
        new_client_id = new_client.get("client_id")
        new_client_secret = new_client.get("client_secret")

        # ── STEP 1-6: Server-to-Server (existing client) ─────────────────────
        print_section("STEPS 1-6: Server-to-Server Auth (client_credentials flow)")
        resp = client.post(f"{AUTH_SERVER}/token/client-credentials", json={
            "client_id": "service-client-001",
            "client_secret": "my-super-secret-value",
            "scope": "ro rw",
            "grant_type": "client_credentials"
        })
        print_result("Client Credentials Token Request", resp)
        service_token = resp.json().get("access_token", "")

        # ── STEP 7-10: Use service token to call resource server ─────────────
        print_section("STEPS 7-10: Service calls Resource Server API")
        headers = {"Authorization": f"Bearer {service_token}"}

        resp = client.get(f"{RESOURCE_SERVER}/api/me", headers=headers)
        print_result("GET /api/me — inspect token claims", resp)

        resp = client.get(f"{RESOURCE_SERVER}/api/data", headers=headers)
        print_result("GET /api/data — requires 'ro' scope", resp)

        resp = client.post(f"{RESOURCE_SERVER}/api/data", json={"key": "value"}, headers=headers)
        print_result("POST /api/data — requires 'rw' scope", resp)

        resp = client.get(f"{RESOURCE_SERVER}/api/admin", headers=headers)
        print_result("GET /api/admin — requires 'admin' role (should FAIL)", resp)

        # ── STEP 1-6: Human user login (alice - admin) ────────────────────────
        print_section("STEPS 1-6: Human User Login — alice (admin)")
        resp = client.post(f"{AUTH_SERVER}/token/login", json={
            "username": "alice",
            "password": "password123",
            "scope": "ro rw admin"
        })
        print_result("Alice Login", resp)
        alice_data = resp.json()
        alice_token = alice_data.get("access_token", "")
        alice_refresh = alice_data.get("refresh_token", "")

        # ── STEP 7-10: Alice uses her token ───────────────────────────────────
        print_section("STEPS 7-10: Alice calls Resource Server")
        headers = {"Authorization": f"Bearer {alice_token}"}

        resp = client.get(f"{RESOURCE_SERVER}/api/me", headers=headers)
        print_result("GET /api/me — Alice's token claims", resp)

        resp = client.get(f"{RESOURCE_SERVER}/api/admin", headers=headers)
        print_result("GET /api/admin — Alice has 'admin' role (should PASS)", resp)

        resp = client.get(f"{RESOURCE_SERVER}/api/finance-report", headers=headers)
        print_result("GET /api/finance-report — ABAC check (admin-group)", resp)

        resp = client.get(f"{RESOURCE_SERVER}/api/reports", headers=headers)
        print_result("GET /api/reports — ACL check", resp)

        # ── Human user login (bob - read only) ───────────────────────────────
        print_section("STEPS 1-6: Human User Login — bob (read-only viewer)")
        resp = client.post(f"{AUTH_SERVER}/token/login", json={
            "username": "bob",
            "password": "bobpass",
            "scope": "ro"
        })
        print_result("Bob Login", resp)
        bob_token = resp.json().get("access_token", "")

        print_section("STEPS 7-10: Bob calls Resource Server")
        headers = {"Authorization": f"Bearer {bob_token}"}

        resp = client.get(f"{RESOURCE_SERVER}/api/data", headers=headers)
        print_result("GET /api/data — Bob has 'ro' scope (should PASS)", resp)

        resp = client.post(f"{RESOURCE_SERVER}/api/data", json={"key": "value"}, headers=headers)
        print_result("POST /api/data — Bob lacks 'rw' scope (should FAIL)", resp)

        resp = client.get(f"{RESOURCE_SERVER}/api/admin", headers=headers)
        print_result("GET /api/admin — Bob lacks 'admin' role (should FAIL)", resp)

        resp = client.get(f"{RESOURCE_SERVER}/api/finance-report", headers=headers)
        print_result("GET /api/finance-report — Bob not in admin-group (should FAIL)", resp)

        # ── Refresh token flow ────────────────────────────────────────────────
        print_section("Refresh Token Flow — Alice gets new access_token")
        resp = client.post(f"{AUTH_SERVER}/token/refresh", json={
            "refresh_token": alice_refresh,
            "grant_type": "refresh_token"
        })
        print_result("Refresh Token Exchange", resp)

        # ── New client (ro only) ──────────────────────────────────────────────
        if new_client_id and new_client_secret:
            print_section("New registered client (ro only) — scope boundary test")
            resp = client.post(f"{AUTH_SERVER}/token/client-credentials", json={
                "client_id": new_client_id,
                "client_secret": new_client_secret,
                "scope": "rw",  # requesting rw but only allowed ro
                "grant_type": "client_credentials"
            })
            print_result("New client requests 'rw' scope (should FAIL — only has 'ro')", resp)

            resp = client.post(f"{AUTH_SERVER}/token/client-credentials", json={
                "client_id": new_client_id,
                "client_secret": new_client_secret,
                "scope": "ro",
                "grant_type": "client_credentials"
            })
            print_result("New client requests 'ro' scope (should PASS)", resp)

if __name__ == "__main__":
    print("\n🔐 OAuth2 / OIDC Full Flow Demo")
    print("Make sure both servers are running:")
    print("  uvicorn auth_server:app --port 8000 &")
    print("  uvicorn resource_server:app --port 8001 &\n")

    try:
        demo()
        print("\n✅ Demo complete!")
    except httpx.ConnectError:
        print("\n❌ Could not connect. Are both servers running on ports 8000 and 8001?")
        sys.exit(1)
```
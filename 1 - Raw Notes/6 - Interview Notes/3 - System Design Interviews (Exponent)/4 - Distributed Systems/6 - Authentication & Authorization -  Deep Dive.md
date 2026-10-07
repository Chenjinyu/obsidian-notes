Date: 2026-02-16
Course: https://www.tryexponent.com/courses/system-design-interviews/authentication-authorization
Tags: [[System Design Interview]] [[Distributed System]] [[6 - Authentication & Authorization]] [[../../../3 - Technologies/Access Control/AuthN & AuthZ|AuthN&Z]]

# Content

## Authentication (AuthN) - Completing Your Picture

**Human/App User:**
- Username + Password
- MFA: TOTP (Google Authenticator), SMS OTP, Email OTP, Hardware keys (YubiKey), Biometrics
- Passkeys (WebAuthn) - passwordless, increasingly common

**Server-to-Server - Beyond OAuth2:**

- **API Keys** - simplest, just a secret string in the header, no token exchange
- **Mutual TLS (mTLS)** - both client and server present certificates to verify each other. Very common in microservices
- **SAML** - older enterprise standard, XML-based, common in corporate SSO (predates OAuth2/OIDC)
- **HMAC Signing** - client signs the request payload with a secret, server verifies the signature (AWS Signature v4 uses this)
- **Basic Auth over HTTPS** - just base64 encoded credentials in the header, simple but less secure
- **Kerberos** - ticket-based, common in Windows/Active Directory environments

One important correction: **OAuth2 itself is actually an authorization framework, not authentication**. What gives you authentication on top of OAuth2 is **OIDC (OpenID Connect)**. OIDC adds an `id_token` (JWT) that carries identity claims. OAuth2 alone just gives you an `access_token` to access resources. Many people conflate these two.

---
## The Three Players You Need to Distinguish
This is where most confusion lives.
```
**Identity Provider (IdP)** Owns and stores user identities. It _knows who you are_. Examples: Active Directory, Okta, Google, Azure AD. When you log in, the IdP verifies your credentials. It answers "who is this person?"
**Authentication Server (AuthN Server)** Handles the login protocol/flow. It talks to the IdP to verify identity and then issues tokens. In many modern systems, the IdP and AuthN server are the same product (e.g., Okta does both). But in enterprise setups, your AuthN server might be Keycloak, which then federates to Active Directory as the IdP backend.
**Authorization Server (AuthZ Server)** Decides what you're allowed to do _after_ identity is confirmed. It issues access tokens with scopes/permissions. In OAuth2/OIDC, this is the token endpoint. Again, often the same product as above but conceptually separate.
```

#### Think of it this way: IdP = the HR records. AuthN server = the security desk that checks your ID. AuthZ server = the door access system that decides which rooms you can enter.

---

## Completing Your Access Control Picture

**RBAC (Role-Based Access Control)** Your understanding is correct. Users are assigned to roles/groups, and permissions are attached to roles, not individuals. AD groups are a classic example. The token typically carries role claims like `roles: ["admin", "read-only"]` and the resource server checks against those.

**ABAC (Attribute-Based Access Control)** More fine-grained than RBAC. Instead of just checking your role, it evaluates a combination of attributes to make a decision. The attributes can come from the user, the resource, or the environment. Example policy: `IF user.department == "finance" AND resource.classification == "financial" AND request.time is business_hours THEN allow`. AWS IAM policies are a good real-world example of ABAC. It's more flexible but also more complex to manage.

**ACL (Access Control List)** Your understanding is right. It's a list attached to a _resource_ specifying which users/entities have what permissions on that specific resource. Think of Linux file permissions (`rwx` per user/group), or sharing a Google Doc with specific people, or the phone app permissions you mentioned. It's resource-centric rather than role-centric.

The key distinction: RBAC asks "what role does this user have?", ABAC asks "do all the attributes match the policy?", ACL asks "is this user listed on this resource's permission list?"

---

## Full End-to-End Flow

Here's the complete picture from client to resource:

```
[User/Client]
     |
     | 1. Login request (credentials / client_id+secret)
     v
[AuthN Server / IdP]  ← may federate to external IdP (e.g., Google, AD)
     |
     | 2. Verify identity
     | 3. If MFA required, challenge and verify second factor
     | 4. Fetch user attributes/groups from IdP/directory
     v
[Authorization Server]
     |
     | 5. Build token with claims (roles, scopes, user attributes)
     | 6. Issue access_token + id_token (OIDC) + refresh_token
     v
[Client holds tokens]
     |
     | 7. API request with Bearer token in Authorization header
     v
[Resource Server / API Gateway]
     |
     | 8. Validate token (signature, expiry, issuer)
     | 9. Extract claims from token
     | 10. Apply AuthZ policy (RBAC/ABAC/ACL check)
     |      - RBAC: does token have required role?
     |      - ABAC: do token attributes satisfy policy?
     |      - ACL: is this user in the resource's permission list?
     v
[Allow or Deny]
```

A few things worth noting in this flow. Step 8 can be done locally by the API (just verifying the JWT signature with the public key, no network call needed) which is one of JWT's main advantages. Step 10 can also involve calling a dedicated policy engine like **OPA (Open Policy Agent)** for complex ABAC rules rather than hardcoding logic in your app. The refresh token in step 6 lets the client get new access tokens without re-authenticating, which is why refresh tokens are treated as much more sensitive than access tokens.

# Note


# Reference

- [[../../../3 - Technologies/Access Control/JWT vs SharedStorage Session Store]]
- [[../../../3 - Technologies/Access Control/Identity & Least Privilege]]
- [[../../../3 - Technologies/Access Control/AuthN & AuthZ|AuthN&Z]]
- [[../../../3 - Technologies/Access Control/Agent-to-app Authorization|Agent-to-app Authorization]]
- 
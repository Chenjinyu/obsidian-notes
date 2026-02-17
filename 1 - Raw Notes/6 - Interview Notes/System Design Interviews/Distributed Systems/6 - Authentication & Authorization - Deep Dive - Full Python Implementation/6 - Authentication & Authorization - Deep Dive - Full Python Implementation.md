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

# Full Python Implementation


# Note


# Reference


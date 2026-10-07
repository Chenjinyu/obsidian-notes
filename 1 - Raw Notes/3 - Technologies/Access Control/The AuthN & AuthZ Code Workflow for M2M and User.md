
## M2M 
```text
+------------+ +-------------------------+ | | 1. Client ID & Client Secret | | | Third-Party|------------------------------>| Identity Provider / | | App | | Authorization Server | | |<------------------------------| | | | 2. ACCESS TOKEN ONLY +-------------------------+ +------------+ | | | | 3. HTTP Header: | 4. Validate Token | Authorization: Bearer <access_token> | (or check signature) v v +----------------------------------------------------------------------+ | Your REST API | +----------------------------------------------------------------------+
```

## User
```text
```
+------------+                 1. Redirect to Login Page               +-------------------------+

|            |-------------------------------------------------------->|                         |
|   User's   |                                                         |    Identity Provider    |
|  Browser / |                 2. User Logs In & Consents              |  (PingFederate/FedSSO)  |
| Mobile App |<--------------------------------------------------------|                         |
|            |                                                         +-------------------------+
|            |                 3. Redirects back with CODE                          ^
|            |<---------------------------------------------------------------------+
+------------+                                                                      |

      |                                                                             |
      | (Passes Code)                                                               |
      v                                                                             |
+------------+                                                                      |

|            |                 4. POST /oauth/token (Exchange Code + Verifier)      |
| App Backend|----------------------------------------------------------------------+
|            |
|            |<---------------------------------------------------------------------+
|            |                 5. Returns BOTH: ID Token & Access Token             |
+------------+                                                                      |

      |                                                                             |
      | 6. Calls API (Attaches Access Token in HTTP Header)                         |
      v                                                                             |
+------------+                                                                      |

|            |                                                                      |
| Your REST  |                 7. Validate Token (Offline check or Introspect)      |
|    API     |----------------------------------------------------------------------+
|            |
+------------+
```

---
```
Date: 2026-02-16
Course: https://www.tryexponent.com/courses/system-design-interviews/authentication-authorization
Tags: [[System Design]] [[Distributed System]] [[6 - Authentication & Authorization]]

# Content

- **Authentication** is the process of proving you are who you say you are when accessing an application. (Who you are)
- **Authorization** is the process of defining and enforcing access policies - that is, what you can do once you're authenticated. (What you can do)
## Why authentication and authorization matter[](https://www.tryexponent.com/courses/system-design-interviews/authentication-authorization#why-authentication-and-authorization-matter)

Keeping data secure means ensuring that the right people (and _only_ the right people) have access to sensitive data. Identifying and vetting users every time access is requested is hard to do, and authentication tools help automate the process.

Authorization goes one step further. For example, say a salesperson needs access to their company's CMS system which stores sensitive customer data. The authentication system will confirm they are legitimate. But do they need access to mergers & acquisitions data? Probably not. An authorization policy ensures that different users have different access depending on their needs.

## How it works[](https://www.tryexponent.com/courses/system-design-interviews/authentication-authorization#how-it-works)

A secure system includes both, and authentication comes first.

### Authentication (or AuthN)

The most common **authentication factors** are usernames and passwords. When the right credentials are given, a system considers the identity valid and grants access. This is known as **1FA** or **single-factor authentication**, and it's considered fairly insecure. Why? Because users are notoriously bad at keeping their login information secure. **Multi-factor authentication (MFA)** is a more secure alternative that requires users to prove their identity in multiple ways. This could be through:

- Single-use PIN numbers
- Authentication apps run by a secure 3rd party
- Biometrics

When choosing an authentication process, there are a few things to keep in mind.

First, remember that security measures shouldn't overly inconvenience users unless they're forced to use your service. Don't ask for biometrics if you're running a free online chess game.

Second, there's an adage in cybersecurity that says "security is only as good as its weakest link." The weakest link is often users. Whether through password apathy, vulnerability to clever phishing schemes, or pure negligence, companies have their work cut out for them. Instituting policies that require good password hygiene can help (requiring long passwords with numbers and special characters, regular password updates, timed log-off, etc.)

Luckily, you don't have to build authentication/authorization platforms yourself. **Auth0** is a well-known platform that sits between your application(s) and **Identity Providers** like Google or Facebook that offer **Single Sign-on (SSO),** connecting and securing you and your data through standard APIs. How? Through a token-based authentication method called **JWT (JSON Web Token)** which is good for stateless applications (and protocols, like HTTP). Another method for authentication over the web uses sessions and cookies.

### Session vs. Token-Based Authentication

Maintaining authentication (without hassling users) across a stateless HTTP connection is an important problem because no one wants to enter their password every time they make a request.

**Session-based authentication** (an older method) relies on the server to track authentication. When a user logs in to a website on a browser, the server creates a **session** for that user. A **session ID** is assigned and stored in a **cookie** in the user's browser, preserving authentication while the user is on the site. Typically, cookies are deleted when a user logs off, but some browsers use **session restoring**, which keeps the session cookies in memory even after the user logs off. Much easier than logging in each time you want to access a page.

**Token-based authentication** is different. When a user logs in, the server creates an encrypted token that allows users to perform any activity on the site. Instead of the server storing session IDs, the client stores the token, either in memory or in a cookie (much like session IDs.)

The main difference between token and traditional session-based authentication is that session-based authentication is very stateful. The server stores the session ID and user info in memory or in a separate session cache, which can become complex as the system or number of users scale.

Token-based authentication is not always stateless, though. Many API tokens are still stored in a database table so they can be verified or revoked.

JWTs are a particularly popular flavor of token-based authentication because they save user data inside the token and can be validated without the database lookups mentioned above. This makes them well-suited for serverless and stateless applications.

JWTs are:

- Small (they transmit quickly)
- Secure (they're asymmetrically encrypted)
- Widely-used (JSON objects are everywhere; virtually all programming languages have JSON parsers, and almost every big web API uses JSON)
- Transparent (their structure makes it easy to verify senders and that contents haven't been tampered with)

JWTs are not without their drawbacks. While they are encrypted, they cannot easily be revoked or invalidated on the server-side, introducing risk. Because of this, they typically use shorter expiration times.

### Authorization (or AuthZ)

Once a user is authenticated, we still need to ensure that they're only allowed access to certain resources. Because unauthorized access to sensitive data can be so catastrophic, many companies set up access policies according to the **principle of least privilege**. That is, by default, you're only allowed access to what you absolutely need. A few common ways to segment access are:
```
- **Role-based (RBAC):** Users are assigned to a certain group (or role) that comes with set permissions. Some examples may include "admin", "member" or "owner."
- **Attribute-based (ABAC):** Users are permitted access according to attributes like title, certification, training, and/or environmental factors like location. Sometimes known as "policy-based access control" or PBAC.
- **Access Control Lists (ACL):** Each user or entity has individual permissions that can be turned on or off, similar to installing a new app on your phone and deciding which permissions to grant (location services, contacts, etc.)

```
ACL is typically used at a more granular level than either ABAC or RBAC - for example, to grant individual users access to a certain file. ABAC and RBAC are generally instituted as company-wide policies.

RBAC is simple. Our salesperson above would probably be given access to a set of customer data according to their territory. ABAC is more flexible and adaptable to events. Say a security breach happens and it's all-hands-on-deck for the infosec team. There may not be an existing role that grants access to all the systems involved in the breach. Someone would have to create a new role and change each infosec team member's role assignment under RBAC. This should be easier under ABAC, but of course, it all depends on how the policies are written. Another common use case for ABAC is a situation where users might have multiple attributes with different permissions. For instance, your news app may employ editors who also author individual stories. These two roles need access to different pages. Under ABAC, you could set attributes = editor, author.

### OAuth 2

Outside of a closed business environment, **authorization frameworks** are needed to securely connect users across applications like Facebook and Instagram, or PayPal and your banking app. **OAuth 2** is a popular framework that uses APIs to extend authorization across connected apps.

Let's go through an example. Let's say you've created a personal assistant app that needs access to a user's Gmail. Google supports OAuth 2, so once you've registered the app with Google and set up your APIs, your app would be able to access your users' Gmail accounts without compromising their usernames and passwords. How does this work?

Four roles are defined:

- **Resource Owner or User:** Owns the account and wants to grant read and/or write access to an application. Credentials include a username and password. In the above example, this is a user who wants to use your personal assistant app.
- **Client:** An application that accesses the user's account. It must be authorized by the user and validated by the authorization provider. Credentials include an ID and a client secret (analogous to a username and password, but specific to the client itself.) Your app.
- **Resource Server:** Houses the application and/or data owned by the user. Will allow access to a client if the client has a valid **access token**. Gmail in the above example.
- **Authorization Server**: A 3rd party that verifies the identity of the user and the client, and issues access tokens.

#### 5 Difference Grant Types
There are 5 different **grant types** that OAuth 2 uses. Think of each grant type as a way for an application to get an access token. These are:
- **Authorization code grant** (`"grant_type": "authorization_code"`) : The most common grant type, standard web app flow. User logs in via browser, gets redirected back with a code, app exchanges code for token.
- **Resource owner credentials grant**(`"grant_type": "password"`) Allows a client to sign in directly using the resource owner's password.
- **Client credentials grant**(`"grant_type": "client_credentails"`). Mainly used for server-to-server interactions; no resource-owner interaction required.
- **Implicit grant**(`"grant_type": "implicit"`). This grant type was previously recommended for single page applications which couldn't keep a client secret. This has been superseded PKCE used with a standard authorization code grant.

## When to bring these up in an interview[](https://www.tryexponent.com/courses/system-design-interviews/authentication-authorization#when-to-bring-these-up-in-an-interview)

If you're specifically asked to design an authorization service, be sure to choose carefully (1FA vs. MFA, which factors you'll require if you choose MFA, etc.) because they can have a big impact on the user experience. You have a responsibility to keep sensitive data safe, but you also don't want to drive away users. Otherwise, it's useful to know about existing authentication infrastructure, but it's doubtful you'll be asked specific questions about it.

Authorization policies are less visible to users. If you're building a large, dynamic system in which users' needs change frequently and/or users can embody several different attributes, we recommend going with ABAC, but RBAC works well in simple cases. It's also useful to know how OAuth 2 works if you think you may be asked to design an app that'll interact with identity providers or other apps using APIs. We've linked to the documentation below.

If you're building apps that need access to other services, look into OAuth 2 and standardized API design. There's no need to reinvent the wheel, especially in a system design interview when you probably want to focus on more functional areas.
# Note


# Reference


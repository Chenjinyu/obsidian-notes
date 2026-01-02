Date: 2025-12-01
Course:
Tags: [[React]] [[Frontend]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content

Here’s a clear, engineer-level explanation of **createContext** and **useContext**, and **when you should actually use them**.
---
# ✅ What is `createContext`?
`createContext` creates a **Context object** that lets you share data **without manually passing props down multiple layers** (a.k.a. “prop drilling”).
### Example

```jsx
import { createContext } from "react";

export const AuthContext = createContext();
```

This creates a **context container**.  
But it's **empty** until you provide a value.

---
# ✅ What is a Provider?

Every context comes with a _Provider_ component:

```jsx
<AuthContext.Provider value={...}>
    {children}
</AuthContext.Provider>
```

This is where you _inject_ the state or functions you want to share.

---
# 🔍 What is `useContext`?

`useContext` lets any child component **consume** the context value provided above it in the component tree.
Example:
```jsx
import { useContext } from "react";
import { AuthContext } from "./AuthContext";

const Profile = () => {
  const { user, logout } = useContext(AuthContext);

  return (
    <div>
      Welcome, {user}
      <button onClick={logout}>Logout</button>
    </div>
  );
};
```

---
# 🧠 Why not just use props?

Because without context:
```
<App>
  <Layout>
    <Header>
      <UserProfile />
    </Header>
  </Layout>
</App>
```

If `UserProfile` needs `user`, you'd have to do:
```jsx
<App user={user}>
  <Layout user={user}>
    <Header user={user}>
      <UserProfile user={user} />
    </Header>
  </Layout>
</App>
```

This is called **prop drilling**.  
Context removes that pain.

---
# 🧩 When should you use Context?
Use context when **many components need access to the same state**, especially if they are deep in the component tree.
### Good use cases:

✔ Authentication (`user`, `token`)  
✔ Theme settings (light/dark)  
✔ App-wide language settings (i18n)  
✔ Shopping cart data  
✔ Feature flags  
✔ Global configuration inside big apps

### Not good use cases:
✘ Storing frequently changing data (like animations or mouse positions)  
✘ Cross-component communication when the data changes _too often_  
Context re-renders all consumers — sometimes too slow.

---
# 📌 Full Minimal Example (Simple Auth System)

### 1 – Define the context
```jsx
// AuthContext.js
import { createContext } from "react";

export const AuthContext = createContext();
```

### 2 – Wrap your app with the provider
```jsx
// AuthProvider.js
import { useState } from "react";
import { AuthContext } from "./AuthContext";

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  function login(name) {
    setUser(name);
  }

  function logout() {
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
```

### 3 – Use the context anywhere
```jsx
// Profile.jsx
import { useContext } from "react";
import { AuthContext } from "./AuthContext";

export function Profile() {
  const { user, login, logout } = useContext(AuthContext);

  return (
    <div>
      {!user && <button onClick={() => login("JC")}>Login</button>}
      {user && (
        <>
          <p>Welcome {user}</p>
          <button onClick={logout}>Logout</button>
        </>
      )}
    </div>
  );
}
```

### 4 – Wrap your root
```jsx
import { AuthProvider } from "./AuthProvider";

root.render(
  <AuthProvider>
    <App />
  </AuthProvider>
);
```

---
# 🎯 Summary (Tough Interview-Level)

|Concept|Purpose|When to Use|
|---|---|---|
|**createContext**|Creates a shared state container|When you want global-ish state|
|**Provider**|Injects the shared value|App wrapper for authentication, theme, config|
|**useContext**|Reads the shared state|Components that need that global value|

Use context **to avoid prop drilling** and **share state across the tree**.

---
If you want, I can also show you:

✅ How to replace context with Zustand or Redux  
✅ How to avoid unnecessary re-renders  
✅ How to type context with TypeScript (very useful!)

# Note


# Reference


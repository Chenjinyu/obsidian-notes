Date: 2025-12-02
Course:
Tags: 
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content

Great — these three topics are **fundamental** to mastering React and Next.js.  
I’ll explain each one clearly, with examples and mental models you can reuse.

---

# ✅ 1) Why `useEffect(() => {}, [])` runs twice in React _Strict Mode_

In development mode only (not production), React 18's Strict Mode has a feature called:
### **“Double rendering of effects”**

This means:
### 👉 React renders your component **twice**, and runs your `useEffect` twice:
- first: mount → run effect
- second: unmount → run cleanup
- third: mount → run effect again  
    (This second mount is to check if your effect is safe and won't cause bugs.)
    
### 🎯 Why React does this?
To detect **unsafe side effects**, such as:
- duplicate event listeners
- accidental state mutations
- memory leaks
- network requests triggered twice
- unsubscribing incorrectly
- effects that aren’t idempotent (safe if repeated)

Strict mode’s double-execution helps catch mistakes that would break in real apps.
### 🔍 Important

**This happens ONLY in development mode.  
In production, the effect runs exactly once.**

---

## 🧠 Visual Timeline (Dev Mode)

```
Mount #1 → useEffect runs
Unmount #1 → cleanup runs
Mount #2 → useEffect runs again
(then normal behavior)
```

So if you see double logs in console:  
**it's React testing your effect, not a bug.**

---

# ✅ 2) How effects differ between Server and Client Components in Next.js

In Next.js 13+ with the App Router:
### ✔ Server Components (default)
- run **only on server**
- **cannot use useEffect**
- cannot access browser APIs (window, document)
- rendered to HTML on the server
Example:

```jsx
// Server Component (default)
export default function Home() {
  // ❌ Cannot use useEffect
  return <div>Hello</div>;
}
```

### ✔ Client Components (`"use client"`)
- run in the browser
- CAN use:
    - useEffect
    - useState
    - useRef
    - event listeners
        
Example:
```jsx
"use client";

export default function Page() {
  useEffect(() => {
    console.log("This runs in browser");
  }, []);
}
```

---

## 🧠 Important: What is actually happening in Next.js?

### Server Component lifecycle:
1. Runs on server → generates static or dynamic HTML
2. Sent to browser
3. Browser only displays markup (no JS in SC)

### Client Component lifecycle:
1. Rendered on server initially
2. Hydrated on client
3. Effects run AFTER hydration in browser

That means:
### ❗ Even Client Components do NOT run effects on the server
Effects run only in the browser.
### 💡 So `useEffect` always runs:
- **After hydration**
- **On the client side only**

---
# 📌 Why does Next.js split this?
Server Components:
- faster, smaller bundle
- no hydration cost
- secure (can access DB directly)
Client Components:
- interactive
- controlled from hooks
Use this rule:

### **Default everything as Server Component unless it NEEDS client-side logic.**

---

# ✅ 3) How to debug infinite loops in `useEffect`

The MOST common React bug:

```jsx
useEffect(() => {
  setState(value)  // causes infinite re-render
}, [value]);
```

Why?  
Because `setState` → triggers re-render → effect dependency changes → effect runs again → loop forever.

---

# ✔ Checklist for Debugging Infinite Loops

## ❌ Mistake #1: Updating state inside an effect that depends on that state

```jsx
useEffect(() => {
  setCount(count + 1); // BAD
}, [count]);
```

Fix → remove dependency or avoid state update:

```jsx
useEffect(() => {
  setCount(c => c + 1);
}, []);  // only once
```

---

## ❌ Mistake #2: Using objects/arrays/functions in dependency array

This effect runs on every render:

```jsx
useEffect(() => {}, [{}]);
```

Why?  
`{}` is a NEW object every render → dependency changes → effect runs again.

Fix → memoize:

```jsx
const config = useMemo(() => ({}), []);
useEffect(() => {}, [config]);
```

---

## ❌ Mistake #3: Fetching data and writing state inside an effect with no memo

```jsx
useEffect(() => {
  fetch("/api/data")
    .then(res => res.json())
    .then(data => setData(data));
});
```

Without `[]`, the effect runs after every render → infinite loop.

Fix:

```jsx
useEffect(() => {
  fetch("/api/data")
    .then(res => res.json())
    .then(data => setData(data));
}, []); // run once
```

---

# 💡 Pro debugging tips from senior engineers

### ✔ Add console logs to see lifecycle:

```jsx
useEffect(() => {
  console.log("Effect Run");

  return () => console.log("Cleanup Run");
}, [value]);
```

### ✔ Use React DevTools → “Profiler”

It visually shows why a component re-rendered.

### ✔ Memoize everything that is passed as dependency:

- `useCallback`
    
- `useMemo`
    

---

# 🎯 Summary

## 🔵 **Strict Mode Double Effect**

- useEffect runs twice in dev
    
- To detect unsafe side effects
    
- Not in production
    

## 🔵 **Next.js Server vs Client Components**

- Server Components → no effects, no browser APIs
    
- Client Components → effects run only in browser after hydration
    

## 🔵 **Debugging Infinite Loops**

- Do not update state in effects that depend on that state
    
- Memoize objects, arrays, functions
    
- Ensure effect dependencies are correct
    


# Note


# Reference


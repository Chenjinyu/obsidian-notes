Date: 2025-12-02
Course:
Tags: 
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content

# 🚀 **React Hooks Cheat Sheet (2025 Edition)**
### Covering All Core + Common Hooks with explanations + examples + when to use
---
# 🟦 **State Hooks**
## 1) `useState`
Store and update local state.
```js
const [count, setCount] = useState(0);
```

✔ When to use:
- Form fields
- UI toggles (modal open, dropdown open)
- Counters
- Any “local state” that belongs only to this component

---
# 🟪 **Effects Hooks**
## 2) `useEffect`
Run side effects _after_ rendering.
```js
useEffect(() => {
  console.log("ran");
}, [deps]);
```

✔ Use for:
- Fetch data
- Event listeners
- Timers
- LocalStorage
- Logging
- Syncing with external systems

❌ Not for:
- Computing derived values
- Updating state unnecessarily
- Anything that can be done in render

---
## 3) `useLayoutEffect`
Like `useEffect`, but runs **before the browser paints**.
```js
useLayoutEffect(() => {
  // measure layout, sync styles
});
```

✔ Use when:
- Measuring DOM sizes (offsetHeight, getBoundingClientRect)
- Preventing visual flicker
- Syncing scroll

---

# 🟩 **Memoization Hooks**

## 4) `useMemo`
Memoize expensive calculations.
```js
const value = useMemo(() => computeExpensive(a), [a]);
```

✔ Use when:
- Heavy computation
- Avoid recomputation
- Stabilizing dependency arrays

---

## 5) `useCallback`
Memoize functions.
```js
const onClick = useCallback(() => {
  console.log(value);
}, [value]);
```

✔ Use when:
- Passing callbacks into child components
- Avoid child re-renders
- Stabilize dependencies inside `useEffect`

---

## 6) `useDeferredValue`

Defer low priority state.
```js
const deferredQuery = useDeferredValue(query);
```

✔ Use when:
- Large UI updates should feel smooth
- Search filters
- Typing shouldn’t lag

---

## 7) `useTransition`
Mark state updates as non-blocking.
```js
const [isPending, startTransition] = useTransition();
```

✔ Use when:
- Navigating lists
- Big view changes
- Slow renders that shouldn’t block input

---
# 🟧 **Refs & DOM Hooks**

## 8) `useRef`
Store mutable values or reference DOM elements.
```js
const inputRef = useRef(null);
<input ref={inputRef} />;
```

✔ Use for:
- DOM access
- Storing values between renders (like instance variables)
- Avoiding useEffect in some cases

---

## 9) `useImperativeHandle`

Customize what parent gets when using `ref`.
```js
useImperativeHandle(ref, () => ({
  focus() {
    inputRef.current.focus();
  }
}));
```

✔ Use when:
- Building reusable component libraries
- Exposing imperative methods

---

## 10) `useId`
Generate stable IDs for accessibility.

```js
const id = useId();
```

✔ Use for:
- Form input + label pairing
- HTML element identifiers

---

# 🟨 **Context Hooks**

## 11) `useContext`
Consume a context value.
```js
const user = useContext(UserContext);
```

✔ Use when:
- Auth
- Theme
- Current language
- Global config
- Avoiding props drilling

---

## 12) `useReducer`

Alternative to useState for complex logic.

```js
const [state, dispatch] = useReducer(reducer, initialState);
```

✔ Use when:
- Multiple related values
- Complex updates
- State machines
- Replacing Redux in small components

---

# 🟫 **Concurrent React & Suspense Hooks**

## 13) `use`
Consume a promise or context directly in React (React 18+).
```js
const data = use(fetchData());
```

✔ Use when:
- Using Server Components
- Using Suspense for async fetching

---

## 14) `useSyncExternalStore`
Subscribe to external stores (Redux, Zustand, custom stores).
```js
const snapshot = useSyncExternalStore(subscribe, getSnapshot);
```

✔ Use when:
- External global state
- Browser APIs as stores
- Window.location, websocket states

---

# 🟩 **Next.js App Router Special Hooks**

(These are not React hooks, but commonly used with client components)
## `useRouter`, `usePathname`, `useSearchParams` (client only)

✔ Use for navigation, reading URLs, updating search params.

---

# 🟦 **Hooks You Rarely Need**
### `useImperativeHandle`
### `useLayoutEffect`
### `useSyncExternalStore`
These are “escape hatches” — powerful but dangerous.
---

# 🧠 Master-Level Mental Model

### 🟢 **useState** → store data
### 🟢 **useEffect** → sync with outside world
### 🟢 **useMemo/useCallback** → optimization & stability
### 🟢 **useRef** → store non-rendered values or DOM
### 🟢 **useContext/useReducer** → shared or complex state
### 🟢 **useTransition** → smoother UI
### 🟢 **useLayoutEffect** → run before painting
### 🟢 **useDeferredValue** → avoid typing lag
### 🟢 **useSyncExternalStore** → external state libraries
---

# Note


# Reference


Date: 2025-11-21
Course:
Tags: [[React]] [[Frontend]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content
Here are the most popular React APIs you should know:
## Core Hooks (React 16.8+)
**State Management**

- `useState` - Add state to functional components
- `useReducer` - Complex state logic with actions/reducers
- `useContext` - Access context values

**Side Effects & Lifecycle**

-  [[useEffect]] - Side effects, subscriptions, data fetching
- `useLayoutEffect` - Synchronous effects (runs before paint)
- `useInsertionEffect` - For CSS-in-JS libraries (rare use)

**Performance Optimization**

- `useMemo` - Memoize expensive calculations
- `useCallback` - Memoize function references
- `memo` - Prevent unnecessary re-renders of components

**Refs & DOM**

- `useRef` - Persist values across renders, access DOM
- `useImperativeHandle` - Customize ref value exposed to parent
- `forwardRef` - Pass refs through components

**Other Hooks**

- `useId` - Generate unique IDs for accessibility
- `useDebugValue` - Custom hook debugging in DevTools
- `useDeferredValue` - Defer updating non-urgent parts of UI
- `useTransition` - Mark state updates as non-urgent

## React 19 New Hooks

- `use` - Read resources like Promises and Context
- `useActionState` - Manage form state with actions
- `useFormStatus` - Access parent form submission status
- `useOptimistic` - Show optimistic UI updates

## Component APIs

- `React.lazy` - Code splitting / lazy load components
-  [[Suspense]] - Show fallback while loading async content
- `Fragment` / `<>` - Group elements without extra DOM nodes
- `StrictMode` - Highlight potential problems in development
- `Profiler` - Measure rendering performance

## Context API

- `createContext` - Create context object
- `Context.Provider` - Provide context value to tree
- `useContext` - Consume context in functional components

## Legacy APIs (Class Components)

- `Component` - Base class for class components
- `PureComponent` - Component with shallow prop/state comparison
- `createRef` - Create refs in class components

## Utilities

- `createElement` - Create React elements programmatically
- `cloneElement` - Clone and modify elements
- `isValidElement` - Check if value is React element
- `Children` - Utilities for manipulating `props.children`
- `startTransition` - Mark updates as transitions (non-hook version)

## Most Commonly Used (Daily Basis)

If you're starting out, focus on these first:

1. `useState`, `useEffect`, `useContext`
2. `useRef`, `forwardRef`
3. `useMemo`, `useCallback`, `memo`
4. `lazy`, `Suspense`
5. `createContext`

The others become important as you encounter specific use cases!


# Note


# Reference


Date: 2025-11-28
Course:
Tags: [[React]] [[Frontend]] 
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content
`<React.Suspense>` is a React component that handles **loading states** for components that load asynchronously. Here's what it does:

## Basic Concept

It shows a **fallback UI** (like a loading spinner) while waiting for something to load.

```tsx
<React.Suspense fallback={<p>Loading...</p>}>
  <SomeAsyncComponent />
</React.Suspense>
```

**What happens:**

1. React starts rendering `<SomeAsyncComponent />`
2. If it's not ready yet (still loading), show `<p>Loading...</p>`
3. Once loaded, replace the fallback with the actual component

## Common Use Cases

**1. Lazy Loading Components (Code Splitting)**

```tsx
import React, { lazy, Suspense } from 'react';

// Component is only loaded when needed
const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<div>Loading component...</div>}>
      <HeavyComponent />
    </Suspense>
  );
}
```

**2. Server Components in Next.js (Async Data)**

```tsx
// app/page.tsx
import { Suspense } from 'react';

async function UserData() {
  const data = await fetch('https://api.example.com/user');
  const user = await data.json();
  return <div>{user.name}</div>;
}

export default function Page() {
  return (
    <Suspense fallback={<p>Loading user...</p>}>
      <UserData />
    </Suspense>
  );
}
```

**3. Multiple Suspense Boundaries**

```tsx
<div>
  <Suspense fallback={<Spinner />}>
    <ProfileHeader />
  </Suspense>
  
  <Suspense fallback={<Skeleton />}>
    <Posts />
  </Suspense>
  
  <Suspense fallback={<Loading />}>
    <Comments />
  </Suspense>
</div>
```

Each section loads independently!

## How It Works

```tsx
<Suspense fallback={<LoadingSpinner />}>
  <AsyncComponent />
</Suspense>
```

**Timeline:**

```
Initial render:
  → Shows: <LoadingSpinner />

Component loads:
  → Shows: <AsyncComponent />
```

## Real-World Example

**Streaming data in Next.js:**

```tsx
import { Suspense } from 'react';

async function RecentPosts() {
  const posts = await fetchPosts(); // This takes time
  return <PostList posts={posts} />;
}

async function TrendingPosts() {
  const trending = await fetchTrending(); // This takes time
  return <TrendingList posts={trending} />;
}

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      
      {/* Recent posts load independently */}
      <Suspense fallback={<div>Loading recent posts...</div>}>
        <RecentPosts />
      </Suspense>
      
      {/* Trending loads independently */}
      <Suspense fallback={<div>Loading trending...</div>}>
        <TrendingPosts />
      </Suspense>
    </div>
  );
}
```

**Benefits:**

- User sees the page immediately
- Content streams in as it's ready
- Faster perceived performance

## Props

```tsx
<Suspense 
  fallback={<LoadingUI />}  // Required: What to show while loading
>
  {children}  // The async content
</Suspense>
```

## With Error Boundaries

Often used together for complete error handling:

```tsx
import { Suspense } from 'react';
import { ErrorBoundary } from 'react-error-boundary';

<ErrorBoundary fallback={<ErrorUI />}>
  <Suspense fallback={<LoadingUI />}>
    <AsyncComponent />
  </Suspense>
</ErrorBoundary>
```

## Key Points

1. **Fallback is required** - you must provide what to show while loading
2. **Automatic** - React handles the switching automatically
3. **Nested** - you can nest multiple Suspense boundaries
4. **Streaming** - In Next.js, enables progressive rendering
5. **User experience** - Shows something immediately instead of blank screen

## Difference from Loading States

**Without Suspense:**

```tsx
function Component() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  
  useEffect(() => {
    fetch('/api/data')
      .then(r => r.json())
      .then(d => {
        setData(d);
        setLoading(false);
      });
  }, []);
  
  if (loading) return <p>Loading...</p>;
  return <div>{data}</div>;
}
```

**With Suspense (simpler):**

```tsx
async function Component() {
  const data = await fetch('/api/data').then(r => r.json());
  return <div>{data}</div>;
}

// Usage:
<Suspense fallback={<p>Loading...</p>}>
  <Component />
</Suspense>
```

**TL;DR:** Suspense shows a loading UI while waiting for async components/data to load, then automatically swaps in the real content when ready. It makes progressive loading and code splitting much easier!


# Note


# Reference


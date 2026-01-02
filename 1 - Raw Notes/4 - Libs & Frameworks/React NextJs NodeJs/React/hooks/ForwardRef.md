Date: 2025-11-21
Course:
Tags: [[React]] [[Hook]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content
## What is `React.forwardRef`?

`React.forwardRef` is a React API that allows a component to **pass a `ref` down to a child element**. It's necessary because refs don't automatically pass through components like regular props do.

## The Problem It Solves

Normally, you can't do this:

```typescript
function MyButton(props) {
  return <button className="my-button">{props.children}</button>;
}

// This WON'T work - ref doesn't reach the <button>
<MyButton ref={buttonRef}>Click me</MyButton>
```

The `ref` gets lost because React treats it specially (like `key`), not as a regular prop.

## The Solution

`forwardRef` lets you explicitly forward the ref:

```typescript
const MyButton = React.forwardRef((props, ref) => {
  return <button ref={ref} className="my-button">{props.children}</button>;
});

// Now this WORKS - ref reaches the <button>
<MyButton ref={buttonRef}>Click me</MyButton>
```

## Real-World Example

```typescript
const FancyInput = React.forwardRef<HTMLInputElement, { label: string }>((props, ref) => {
  return (
    <div>
      <label>{props.label}</label>
      <input ref={ref} type="text" />
    </div>
  );
});

// Usage
function Parent() {
  const inputRef = useRef<HTMLInputElement>(null);
  
  const focusInput = () => {
    inputRef.current?.focus(); // Direct access to the <input> element!
  };
  
  return (
    <>
      <FancyInput ref={inputRef} label="Name" />
      <button onClick={focusInput}>Focus input</button>
    </>
  );
}
```

## When to Use It

Use `forwardRef` when:

- Building **reusable component libraries** (like your Toast example)
- You need **parent components to access DOM elements** directly
- Working with third-party libraries that need refs (animations, focus management, etc.)

Without `forwardRef`, users of your component couldn't access the underlying DOM element, limiting what they can do with it!


# Note


# Reference


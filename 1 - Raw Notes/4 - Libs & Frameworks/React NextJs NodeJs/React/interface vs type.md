Date: 2025-12-01
Course:
Tags: 
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content
In React (and TypeScript in general), **`interface`** and **`type`** are very similar — both let you define the structure of objects, component props, hooks, state, etc.
But there are important differences.
Below is the clearest, real-world explanation 👇

---

# ✅ **1. Basic Syntax: Very Similar**
### **Interface**
```ts
interface User {
  id: number;
  name: string;
}
```

### **Type**
```ts
type User = {
  id: number;
  name: string;
};
```
They behave the **same** in most React situations.

---
# ✅ **2. EXTENDING (Key Difference)**
### **Interfaces can be extended multiple times**
```ts
interface A { x: number; }
interface A { y: number; }  // merged!

const obj: A = { x: 1, y: 2 };
```

This is called **declaration merging** — types cannot do this.
### **Types CANNOT merge**
```ts
type A = { x: number };
// ❌ error: duplicate type name
type A = { y: number };
```
---
# ✅ **3. Which one to use for React props?**
### **Either works**, but many React developers prefer interface:
```ts
interface ButtonProps {
  label: string;
  disabled?: boolean;
}

function Button({ label, disabled }: ButtonProps) {
  return <button disabled={disabled}>{label}</button>;
}
```
But using `type` is just as valid:
```ts
type ButtonProps = {
  label: string;
  disabled?: boolean;
};
```
---
# ✅ **4. Types are more powerful for unions**
```ts
type Result = "success" | "error";
```
Interfaces **cannot** do this.

---

# ✅ **5. Types can create complex structures (tuples, unions, mapped types)**
```ts
type ApiResponse<T> = {
  data: T;
  error?: string;
};
```

Interfaces **cannot** express unions:
```ts
type Theme = "light" | "dark";  // ✔ allowed
```

---

# ✅ **6. Interfaces work better with class components**
If you're using a class-based React component:
```ts
interface Props {
  title: string;
}

class Header extends React.Component<Props> {}
```
Type also works, but interface historically feels more natural.

---
# 📌 **Summary Table**

| Feature                    | `interface` | `type` |
| -------------------------- | ----------- | ------ |
| Can describe object shape  | ✔           | ✔      |
| Can extend another one     | ✔           | ✔      |
| Declaration merging        | ✔           | ❌      |
| React component props      | ✔           | ✔      |
| Union types                | ❌           | ✔      |
| Tuples                     | ❌           | ✔      |
| More expressive / flexible | ❌           | ✔      |

---
# 🔥 **When to choose which?**
### ✔ Use **interface** when:
* You expect extensions (like theme config)
* Defining React component props
* Creating public API shapes

### ✔ Use **type** when:
* You need unions (`A | B`)
* You need tuples (`[number, string]`)
* You want complex mapped types
* You want flexible type composition

---
# 🧠 My advice (most React projects follow this):

### **Use `interface` for component props**

### **Use `type` for everything else (unions, utility types, complex shapes)**


# Note


# Reference


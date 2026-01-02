Date: 2025-11-01
Course:
Tags: [[React]] [[JavaScript]] [[TypeScript]] 
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content
Absolutely! Let’s go step by step and make this crystal clear.

---

## 🧩 What is **object destructuring**?

**Object destructuring** in JavaScript/TypeScript is a **syntax that allows you to unpack properties from objects into separate variables**.

Instead of doing this:

```ts
const user = { name: "JC", age: 35 };
const name = user.name;
const age = user.age;
```

You can do it in **one line**:

```ts
const { name, age } = user;
```

* `name` and `age` are **new variables** holding the values from `user.name` and `user.age`.

---

## 🔹 Basic Example

```ts
const user = { name: "JC", age: 35 };

const { name, age } = user;

console.log(name); // JC
console.log(age);  // 35
```

✅ This is simpler and cleaner than assigning each property individually.

---

## 🔹 Renaming variables (aliasing)

Sometimes you want the variable to have a different name:

```ts
const { name: fullName, age: userAge } = user;

console.log(fullName); // JC
console.log(userAge);  // 35
```

* Before the colon: the **property name** in the object.
* After the colon: the **new variable name**.

---

## 🔹 Default values

If a property might not exist, you can provide a default:

```ts
const user = { name: "JC" };

const { name, age = 18 } = user;

console.log(name); // JC
console.log(age);  // 18 (default value)
```

---

## 🔹 Nested objects

If your object has nested objects, you can destructure them too:

```ts
const user = {
  name: "JC",
  address: {
    city: "New York",
    zip: 10001
  }
};

const { name, address: { city, zip } } = user;

console.log(name); // JC
console.log(city); // New York
console.log(zip);  // 10001
```

* You can even **rename nested properties**:

```ts
const { address: { city: userCity } } = user;
console.log(userCity); // New York
```

---

## 🔹 Function parameters

Object destructuring is often used in **function parameters**:

```ts
type User = { name: string; age: number };

function greet({ name, age }: User) {
  console.log(`Hello ${name}, you are ${age} years old.`);
}

greet({ name: "JC", age: 35 });
// Output: Hello JC, you are 35 years old.
```

* Here, the object is destructured **directly in the parameter list**.

---

## 🔹 Combining with arrays

You can mix destructuring:

```ts
const users = [
  { name: "JC", age: 35 },
  { name: "Anna", age: 28 }
];

const [firstUser, secondUser] = users;

console.log(firstUser.name);  // JC
console.log(secondUser.age);  // 28
```

---

### ✅ Summary

| Feature        | Syntax                       | Example                               |
| -------------- | ---------------------------- | ------------------------------------- |
| Basic          | `{ prop } = obj`             | `const { name } = user;`              |
| Rename         | `{ prop: newName } = obj`    | `const { name: fullName } = user;`    |
| Default        | `{ prop = default } = obj`   | `const { age = 18 } = user;`          |
| Nested         | `{ outer: { inner } } = obj` | `const { address: { city } } = user;` |
| Function param | `fn({prop})`                 | `function greet({name}) {}`           |

---

If you want, I can make a **diagram showing how destructuring works in memory** — it makes it visually clear which variables come from which object properties.

Do you want me to do that?



# Note


# Reference


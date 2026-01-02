Date: 2025-11-11
Course:
Tags: [[Frontend]] [[React]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content

```js
import * as SelectPrimitive from "@radix-ui/react-select";
const SelectTrigger = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Trigger>
  >(({ className, children, ...props }, ref) => (
  <SelectPrimitive.Trigger
    ref={ref}
	className={cn(
	"flex h-9 w-full items-center justify-between whitespace-nowrap rounded-md border border-input bg-transparent px-3 py-2 text-sm,
	className,
  )}
  {...props}
>
  {children}
  <SelectPrimitive.Icon asChild>
  . <CaretSortIcon className="h-4 w-4 opacity-50" />
    </SelectPrimitive.Icon>
  </SelectPrimitive.Trigger>
));

SelectTrigger.displayName = SelectPrimitive.Trigger.displayName;
```

convert to python pattern:
```python
def select_trigger(class_name=None, children=None, **props):
    # ref is handled specially
    ref = props.pop('ref', None)
    ...
```
- `className` ↔ a **named argument** (`class_name` in Python)
- `children` ↔ a **parameter** representing inner elements (like child nodes)
- `...props` ↔ Python’s `**props` (variable keyword arguments — “catch everything else”)
- `ref` ↔ an optional argument that’s handled specially by React for direct DOM access

the 
```js
React.forwardRef # is like a decorator in Python - it wraps a function and adds extra behavior.
```

the convert script will like below:
```python
def forward_ref(fn):
	def wrapper(*args, ref=None, **kwargs):
		# inject 'ref' hanlding
		return fn(*arg, ref=ref, **kwargs)
	return wrapper
	
@forward_ref
def select_trigger(class_name=None, children=None, **props):
```

In Typescript, this line defines the type of the arguments and ref, 
In Python, it's roughy like adding type hints:

```python
from typing import Any, TypeVar

RefType = TypeVar("RefType")
PropsType = TypeVar("PropsType")

def forward_ref(fn: Callable[[ProposType, RefType], Any)] -> Callable[..., Any]:
	...
```

So in this line,
- `React.ElementRef<typeof SelectPrimitive.Trigger>` → the type of the `ref` parameter (what element ref points to)
- `React.ComponentPropsWithoutRef<typeof SelectPrimitive.Trigger>` → type of props your component receives (everything except `ref`)
It’s purely for **type safety and autocompletion**, similar to Python’s `typing` module.

### The destructuring syntax
```tsx
({ className, children, ...props }, ref)
```

is equivalent to unpacking arguments like this in Python:

```python
def select_trigger(args, ref):
    class_name = args.get("className")
    children = args.get("children")
    props = {k: v for k, v in args.items() if k not in ["className", "children"]}
```

### TL;DR Mapping Table
|React/TypeScript Concept|Python Equivalent|Meaning|
|---|---|---|
|`React.forwardRef()`|Decorator (`@forward_ref`)|Wraps a function to handle refs|
|`({ className, children, ...props })`|`def f(class_name=None, children=None, **props)`|Destructures props|
|`ref` parameter|Extra decorator-handled argument|DOM reference|
|`{...props}`|`**props` unpacking|Pass all remaining keyword args|
|Generics `<T, U>`|`TypeVar` or type hints|Static typing / IDE help|

# Note


# Reference


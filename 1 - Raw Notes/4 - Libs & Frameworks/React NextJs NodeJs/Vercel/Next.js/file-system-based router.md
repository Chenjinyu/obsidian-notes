Date: 2025-11-13
Course:
Tags: [[NextJs]] [[Vercel]] [[Frontend]] [[AI SDK]] [[AI Agent]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content
This is one of those **magical-looking things** in Next.js + Vercel AI SDK that’s actually very logical once you unpack it.
Let’s go step-by-step so you can see exactly **how `Page` triggers the `POST` function in `app/api/summarize/route.ts`**.

---
## 🧩 1. The key: `useChat({ api: '/api/summarize' })`
In your frontend:
```tsx
const { messages, append } = useChat({
  api: '/api/summarize',
});
```
This line tells the Vercel **AI SDK hook** (`useChat`) which endpoint it should call when you send a message.
- `api: '/api/summarize'` means:  
    → Send chat data to **`/api/summarize`** endpoint.
- The `useChat` hook automatically performs an HTTP `POST` request to that endpoint.
So, when you do:
```tsx
append({ role: 'user', content: text });
```
It runs something equivalent to:
```ts
fetch('/api/summarize', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ messages: [...previous, newMessage] }),
});
```
That’s how the frontend → backend connection happens.

---
## ⚙️ 2. Next.js routing system

Next.js uses a **file-system-based router**.  
This means that the URL path corresponds directly to a file in the `/app` directory.
Your file path:
```
app/api/summarize/route.ts
```
automatically maps to the URL:
```
/api/summarize
```

✅ So:
- File name: `route.ts`
- Folder path: `/app/api/summarize/`
- HTTP method: function name (`POST`, `GET`, etc.)
    
Example:
```ts
// app/api/summarize/route.ts

export async function POST(req: Request) {
  // handle POST requests to /api/summarize
}
```
This function will be **invoked automatically** whenever the client calls `/api/summarize` with a POST request.

---
## 🧠 3. How Vercel AI SDK wraps it

**When using `useChat`, the SDK expects your endpoint to:**
- **Accept a POST request,**
- **Receive JSON `{ messages: [...] }` or `{ input: ... }`,**
- **And return either:**
    - **JSON (static response), or**
    - **a streaming response (for real-time AI outputs).**
**It’s designed to integrate directly with `/api/` routes in Next.js.**

So the entire flow looks like this:
```
User clicks “Summarize”
   ↓
React calls append() → useChat()
   ↓
useChat() makes POST /api/summarize
   ↓
Next.js finds app/api/summarize/route.ts
   ↓
Executes export async function POST(req)
   ↓
Your backend code runs (OpenAI, KV, etc.)
   ↓
Response returns → useChat updates UI
```

---
## 💡 Analogy (Python version)

If you’re from Python/Flask background, think like this:
```python
@app.route('/api/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    return jsonify(result="summary here")
```
And your frontend `fetch("/api/summarize", { method: "POST" })`  
automatically calls this route.

Next.js + Vercel AI SDK just _hide this wiring_ behind `useChat()`.

---

Would you like me to show what the `useChat` hook source roughly looks like internally (to see how it triggers the API)?


# Note


# Reference


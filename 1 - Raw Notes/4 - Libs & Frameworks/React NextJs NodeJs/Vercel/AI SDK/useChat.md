Date: 2025-11-13
Course:
Tags:  [[NextJs]] [[Vercel]] [[Frontend]] [[AI SDK]] [[AI Agent]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content
Perfect 👌 — let’s **peek under the hood** of what the `useChat()` hook from **Vercel’s AI SDK** actually does.

I’ll show you a simplified version that captures the essence (in TypeScript-style pseudocode, not the full implementation).

---
## 🧠 What `useChat()` really is
Under the hood, it’s just a **React hook** that manages:
- Your chat message state,
- Sending new messages to the backend (`/api/...`),
- Receiving streaming or static responses,
- Updating the UI in real time.
---
### 🧩 Simplified Implementation Example
```ts
import { useState } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export function useChat({ api }: { api: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  async function append(newMessage: Message) {
    // 1. Add the user's message to the local state
    setMessages((prev) => [...prev, newMessage]);
    setIsLoading(true);

    try {
      // 2. Send the message list to the backend (POST)
      const res = await fetch(api, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: [...messages, newMessage],
        }),
      });

      // 3. Handle response
      const reader = res.body?.getReader();
      const decoder = new TextDecoder();

      let aiResponse = "";

      // 4. (Optional) Stream the response token by token
      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          aiResponse += decoder.decode(value);
          // update the last assistant message in UI as we stream
          setMessages((prev) => {
            const updated = [...prev];
            if (
              updated.length &&
              updated[updated.length - 1].role === "assistant"
            ) {
              updated[updated.length - 1].content = aiResponse;
            } else {
              updated.push({ role: "assistant", content: aiResponse });
            }
            return updated;
          });
        }
      } else {
        // 5. If response not streaming, just parse JSON
        const data = await res.json();
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: data.summary },
        ]);
      }
    } finally {
      setIsLoading(false);
    }
  }

  // 6. Expose helpers
  return { messages, append, isLoading };
}
```

---
## ⚙️ How it connects to your `POST` endpoint
When you call:
```tsx
append({ role: 'user', content: text });
```
The hook:
1. Updates local state immediately (optimistic UI).
2. Sends a `POST` request to your backend endpoint:
    ```bash
    POST /api/summarize
    Content-Type: application/json
    
    {
      "messages": [
        { "role": "user", "content": "Summarize this article..." }
      ]
    }
    ```
1. Waits for your backend to respond (either all at once or streamed).
2. Adds the assistant’s reply to the chat.
    
---
## 🧩 The Backend Side (Your Code)
Your file:
```ts
// app/api/summarize/route.ts

export async function POST(req: Request) {
  const { messages } = await req.json();
  // do something (e.g. OpenAI API)
  return NextResponse.json({ summary: "AI response..." });
}
```
This matches exactly what the hook sends.  
Next.js automatically maps this to `/api/summarize`.

---
## 🎁 Bonus: The Real Vercel AI SDK Does More

In reality, the actual `useChat` from Vercel:
- Supports **SSE (Server-Sent Events)** for streaming,
- Handles **abort signals** for canceling mid-response,
- Provides `input`, `handleInputChange`, and `handleSubmit` helpers,
- Persists chat state to localStorage (optional),
- Supports custom API routes (like `/api/ask`),
- Works seamlessly with `useCompletion()` for non-chat use cases.

---
✅ **Summary of the flow**
```
React Component (useChat)
   ↓
append() → fetch("/api/summarize", { method: "POST", body: {...} })
   ↓
Next.js API Route (/app/api/summarize/route.ts)
   ↓
Your POST function executes
   ↓
Response streamed or returned → Hook updates UI
```
---

Would you like me to show you **how the backend can return a streaming response** (so the user sees the text being typed out token-by-token, like ChatGPT)?


# Note


# Reference


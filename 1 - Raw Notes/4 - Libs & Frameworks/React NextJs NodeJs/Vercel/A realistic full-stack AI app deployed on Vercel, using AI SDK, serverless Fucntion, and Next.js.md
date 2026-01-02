Date: 2025-11-13
Course:
Tags: [[Vercel]] [[Frontend]] [[Severless]] [[Next.js]] [[AI SDK]] [[AI Agent]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content

This turns your app from a _stateless summarizer_ into a _persistent chat assistant_ that remembers user history across sessions.
---
## 🧱 1. Install Vercel KV
Vercel KV is a **managed Redis database** built on Upstash, tightly integrated with Vercel’s platform.
```bash
npm install @vercel/kv
```
Then, go to your [Vercel dashboard → Storage → KV](https://vercel.com/dashboard/stores) and create a new **KV database**.  
Once it’s ready, copy the **Environment Variables** (you’ll see four):
```
KV_URL=...
KV_REST_API_URL=...
KV_REST_API_TOKEN=...
KV_REST_API_READ_ONLY_TOKEN=...
```
Add them to your project (in `.env.local`):
```bash
# .env.local
OPENAI_API_KEY=sk-xxxx
KV_URL=...
KV_REST_API_URL=...
KV_REST_API_TOKEN=...
KV_REST_API_READ_ONLY_TOKEN=...
```

---
## 🧠 2. Modify the Serverless API with Memory

Let’s store each user’s chat history in KV and retrieve it when generating summaries.
`app/api/summarize/route.ts`
```ts
import { NextResponse } from 'next/server';
import OpenAI from 'openai';
import { kv } from '@vercel/kv';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY!,
});

export async function POST(req: Request) {
  const { text, userId } = await req.json();

  // Retrieve chat history for this user
  const historyKey = `chat:${userId}`;
  const history = (await kv.get<string[]>(historyKey)) || [];

  // Append new user message
  history.push(`User: ${text}`);

  // Generate AI response with context
  const completion = await openai.chat.completions.create({
    model: 'gpt-4o-mini',
    messages: [
      { role: 'system', content: 'You are a summarizer that remembers prior discussions.' },
      ...history.map((h) => ({ role: 'user', content: h })),
    ],
  });

  const summary = completion.choices[0].message.content ?? 'No summary available.';

  // Store updated history (trim if too long)
  history.push(`Assistant: ${summary}`);
  if (history.length > 10) history.splice(0, history.length - 10);
  await kv.set(historyKey, history);

  return NextResponse.json({ summary });
}
```

✅ The chat context now persists in Redis via KV.

---
## 🧩 3. Update the Frontend
`app/page.tsx`
```tsx
'use client';

import { useState } from 'react';
import { useChat } from 'ai/react';

export default function Page() {
  const [userId] = useState('user123'); // In real app, use auth ID
  const [text, setText] = useState('');

  const { messages, append, isLoading } = useChat({
    api: '/api/summarize',
    body: { userId },
  });

  return (
    <main className="flex flex-col p-6 max-w-lg mx-auto">
      <h1 className="text-xl font-bold mb-4">AI Chat Summarizer (with Memory)</h1>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text to summarize..."
        className="border p-2 rounded"
      />
      <button
        disabled={isLoading}
        onClick={() => append({ role: 'user', content: text })}
        className="bg-blue-600 text-white p-2 rounded mt-3"
      >
        Summarize
      </button>

      <div className="mt-4 space-y-2">
        {messages.map((m, i) => (
          <p key={i} className={m.role === 'user' ? 'text-gray-600' : 'text-green-700'}>
            {m.role === 'assistant' ? '🧠 ' : '🙋 '} {m.content}
          </p>
        ))}
      </div>
    </main>
  );
}
```

✅ Now each conversation round-trip keeps its memory using the same `userId`.

---
## 🧩 4. How the Data Flows
```
[Frontend React] → /api/summarize → [Vercel Function]
                          ↓
                     [Vercel KV Redis]
                          ↓
                 Store + Retrieve chat context
                          ↓
                    [OpenAI Completion]
```

---
## 🔍 5. Benefits of Using Vercel KV

|Feature|Benefit|
|---|---|
|🧠 Persistent Memory|Keep chat context between sessions|
|⚡️ Low Latency|KV sits close to your Vercel edge region|
|🔒 Secure|Built-in auth + per-project isolation|
|💸 Cost-Effective|Pay only for storage & requests|
|🌍 Global|Automatically replicated across regions|

---
## 🌈 6. Optional: Add TTL (Expiration)

You can automatically clear stale conversations:
```ts
await kv.set(historyKey, history, { ex: 3600 }); // expire in 1 hour
```

---
## 🚀 7. Deploy
```bash
vercel deploy
```

Then, you have a live **AI chat with memory** — all on Vercel’s managed cloud.

---

# Note


# Reference


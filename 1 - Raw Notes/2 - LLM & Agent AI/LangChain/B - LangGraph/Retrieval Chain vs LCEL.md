Date: 2025-10-26
Course:
Tags: [[AI]] [[LangGraph]] [[LCEL]] [[AI Agent]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content
# Table Content
1. [create_retrieval_chain vs LCEL](#create_retrieval_chain-vs-lcel)
2. [What create_stuff_documents_chain() is](#what-create_stuff_documents_chain-is)

## create_retrieval_chain vs LCEL
### chain = create_retrieval_chain(retriever, llm) vs chain = retriever | llm
**1. The classical chain:**
```py
chain = create_retrieval_chain(retriever, llm)
```
internally does something like:
```txt
query (user input)
   ↓
retriever (finds relevant docs)
   ↓
combine docs + query → LLM (generates the answer)
   ↓
answer
```

**2. The LCEL (LangChain Expression Language) version**

Yes — you can write this exact logic as a pipeline composition using the | operator:
```py
chain = retriever | llm
```

But there’s an important detail 
The retriever **returns documents, not text** — and the llm expects a string (prompt).
So you usually insert a formatter in between to convert docs → text.

Example:
```py
from langchain_core.runnables import RunnablePassthrough

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | llm
)
```

Then invoke:
```py
result = chain.invoke("What is FAISS?")
```

**3. A cleaner and realistic LCEL RAG chain**

Here’s a minimal, working RAG chain written 100% in LCEL style:
```py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Suppose you already have a retriever (e.g. from FAISS or Pinecone)
# retriever = vectorstore.as_retriever()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_template("""
Answer the question using only the context below.

Context:
{context}

Question:
{question}
""")

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
)

response = chain.invoke("What is FAISS?")
print(response.content)
```

**4. LCEL vs create_retrieval_chain**

| Method                     | Type            | Flexibility | Recommended for        |      |                      |
| -------------------------- | --------------- | ----------- | ---------------------- | ---- | -------------------- |
| `create_retrieval_chain()` | Prebuilt helper | Low         | Beginners, quick setup |      |                      |
| `retriever                 | prompt          | llm` (LCEL) | Fully composable       | High | Custom RAG workflows |


>LCEL is now the preferred approach — it’s more readable, more modular, and integrates better with new patterns (like function calling, agents, and streaming).


---

### 🧩 1. When you use:

```python
chain = create_retrieval_chain(retriever, llm)
```

#### ✅ What happens internally:

* LangChain **creates a default prompt** for you automatically.

* The default is a **Retrieval-QA-style system prompt**, e.g.:

  ```
  Use the following context to answer the question.
  If you don't know the answer, say you don't know.

  Context:
  {context}

  Question:
  {input}
  ```

* Then it builds an internal LCEL pipeline like this:

  ```python
  chain = (
      {"context": retriever, "input": RunnablePassthrough()}
      | default_prompt_template
      | llm
      | StrOutputParser()
  )
  ```

So — you **are** using LCEL internally, but LangChain hides it for convenience.

✅ In short:

> You **don’t need** to manually supply a prompt when using `create_retrieval_chain`, because LangChain provides a sensible default one.


### 🧱 2. But you *can* override the prompt if you want

If you want a customized question-answering style (for example, “Answer as a helpful data analyst” or “Write in JSON format”), you can use:

```python
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

custom_prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant.

Use the following retrieved documents to answer the question.
If unsure, say "I don’t know."

Context:
{context}

Question:
{input}
""")

chain = create_retrieval_chain(retriever, llm, prompt=custom_prompt)
```

Now LangChain replaces its default prompt with yours.


## ⚙️ 3. LCEL equivalent

If you were to build it manually with LCEL, it would look like:

```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

chain = (
    {"context": retriever, "input": RunnablePassthrough()}
    | custom_prompt
    | llm
    | StrOutputParser()
)
```

So the `create_retrieval_chain()` call is **just a prebuilt LCEL composition** — a shortcut.


## ✅ Summary

| Concept           | `create_retrieval_chain()`    | LCEL              |
| ----------------- | ----------------------------- | ----------------- |
| Prompt required?  | ❌ Optional (default included) | ✅ Required        |
| Composition style | Hidden inside function        | Explicit pipeline |
| Flexibility       | Easier                        | Full control      |
| Typical use       | Quick QA, RAG demos           | Custom workflows  |


So:

> **You don’t need to supply a prompt when using `create_retrieval_chain()`**, because it already includes a default LCEL prompt under the hood.
> But you *can* pass one if you want custom reasoning or formatting.

---


## What create_stuff_documents_chain() is

`create_stuff_documents_chain()` is a **lower-level helper function** in LangChain for building a **document-to-answer** chain — it’s the core part that sits **inside** retrieval-based chains.

In simple words:

> It takes a list of retrieved documents, “stuffs” them into a prompt template, and passes that to the LLM to get an answer.

That’s why it’s called a *stuff documents chain* — it literally *stuffs* documents into the context.

### 🧠 1. What it does

Here’s roughly what happens inside:

```python
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant. Use the following context to answer the question.

Context:
{context}

Question:
{input}
""")

stuff_chain = create_stuff_documents_chain(llm, prompt)
```

Under the hood, that’s equivalent to an LCEL chain like:

```python
chain = (
    {"context": lambda docs: "\n\n".join(d.page_content for d in docs), "input": RunnablePassthrough()}
    | prompt
    | llm
)
```

So `create_stuff_documents_chain()` just automates the process of merging retrieved documents into the prompt.

### 🧰 2. When to use it

You’ll use `create_stuff_documents_chain()` when you want **fine-grained control** over your RAG pipeline — for example, when you want to:

* Customize how the documents are combined.
* Reuse your LLM and prompt for other parts of your workflow.
* Manually wire a retriever → LLM pipeline (instead of using `create_retrieval_chain`).

Example:

```python
from langchain.chains import create_retrieval_chain

retrieval_chain = create_retrieval_chain(retriever, stuff_chain)
```

Here’s what happens in that setup:

```
query → retriever → documents → create_stuff_documents_chain → LLM → answer
```

So `create_stuff_documents_chain()` is the **inner document-combining step** inside your retrieval pipeline.

### ⚖️ 3. Comparison with `create_retrieval_chain()`

| Function                         | Purpose                                                     | Handles Retrieval? | Handles Prompt + LLM? | Level      |
| -------------------------------- | ----------------------------------------------------------- | ------------------ | --------------------- | ---------- |
| `create_stuff_documents_chain()` | Stuff documents into a prompt and call LLM                  | ❌ No               | ✅ Yes                 | Low-level  |
| `create_retrieval_chain()`       | Retrieve docs, pass them to a document chain (like “stuff”) | ✅ Yes              | ✅ Yes                 | High-level |

So if you call:

```python
chain = create_retrieval_chain(retriever, llm)
```

LangChain internally does:

```python
stuff_chain = create_stuff_documents_chain(llm, default_prompt)
chain = create_retrieval_chain(retriever, stuff_chain)
```

### ✅ 4. When to use which

| Situation                                                                | Use this                                               |
| ------------------------------------------------------------------------ | ------------------------------------------------------ |
| You just want a working RAG chain (retriever + LLM)                      | `create_retrieval_chain()`                             |
| You want to customize how documents are merged into the prompt           | `create_stuff_documents_chain()`                       |
| You want to experiment with “map-reduce” or “refine” document processing | `create_map_reduce_chain()` or `create_refine_chain()` |


### 🧩 Summary

| Function                         | Description                                           | Example Usage                                                                   |
| -------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------- |
| `create_stuff_documents_chain()` | Combines multiple documents into a prompt for the LLM | When you already have retrieved documents and want to control prompt formatting |
| `create_retrieval_chain()`       | Full retrieval + LLM pipeline                         | When you want a simple end-to-end RAG system                                    |

---




# Note


# Reference


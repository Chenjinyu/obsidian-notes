Date: 2025-10-26
Course:
Tags: [[ML]] [[AI]] [[Vector Storages]] [[Database]] [[Local]]

Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

## NOTE -> It's a local file

# Content
## 🧩 1. `from langchain_community.vectorstores import Pinecone` (old style)

### ✅ What it is:

* This is the **legacy / community integration** that was originally bundled inside `langchain_community`.
* It still works, but it’s considered **deprecated** (will eventually be removed).
* Import path:

  ```python
  from langchain_community.vectorstores import Pinecone
  ```

### 🧱 Internal behavior:

* Uses the `pinecone` Python SDK directly.
* You must manually initialize your Pinecone client and index.
* Example:

  ```python
  from pinecone import Pinecone as PineconeClient
  from langchain_community.vectorstores import Pinecone

  pc = PineconeClient(api_key="your-key")
  index = pc.Index("my-index")

  vectorstore = Pinecone(index, embedding_function, text_key="text")
  ```

## 🚀 2. `from langchain_pinecone import PineconeVectorStore` (new style, recommended ✅)

### ✅ What it is:

* This is the **official modular package** for Pinecone integration with LangChain.
* New structure introduced in 2024 as part of LangChain’s **component modularization** (each integration moved to its own package).
* Install separately via:

  ```bash
  pip install langchain-pinecone
  ```

### 🧠 Import path:

```python
from langchain_pinecone import PineconeVectorStore
```

### 💡 Example usage:

```python
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = PineconeVectorStore(
    index_name="my-index",
    embedding=embeddings,
)

retriever = vectorstore.as_retriever()
```

### 🔍 Key differences from the old one:

| Feature                     | `langchain_community`            | `langchain_pinecone`                       |
| --------------------------- | -------------------------------- | ------------------------------------------ |
| Status                      | Legacy                           | ✅ Official & Current                       |
| Install                     | Built into `langchain_community` | Separate: `pip install langchain-pinecone` |
| API                         | Older `Pinecone()` class         | New `PineconeVectorStore()` class          |
| Type hints / autocompletion | Limited                          | ✅ Fully typed                              |
| Maintenance                 | Frozen                           | ✅ Actively maintained                      |


## ✅ 3. In short:

| Use case                     | Correct import                                          |
| ---------------------------- | ------------------------------------------------------- |
| 🔥 Modern project            | `from langchain_pinecone import PineconeVectorStore`    |
| 🧓 Legacy code (still works) | `from langchain_community.vectorstores import Pinecone` |

---




# Note


# Reference


Date: 2025-10-26
Course:
Tags: [[Vector Storages]] [[Database]] [[AI Agent]] [[Local]] [[Cloud]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

## NOTE -> It can be a local dockerized database.
# Content
## 🧠 Concept Overview

Traditional databases handle **structured data** (numbers, text fields, etc.).
But **Weaviate** handles **unstructured data** — text, images, audio, video — by converting them into **vector embeddings**.

Then you can:

* **Search semantically** (find similar meaning, not just keyword matches)
* **Retrieve context for LLMs (RAG)**
* **Classify or cluster** data by similarity


**Weaviate** is an open-source, cloud-native vector database that stores both objects and vectors, enabling semantic search at scale. It combines vector similarity search with keyword filtering, retrieval-augmented generation (RAG), and reranking in a single query interface. Common use cases include RAG systems, semantic and image search, recommendation engines, chatbots, and content classification.

Weaviate supports two approaches to store vectors: automatic vectorization at import using [integrated models](https://docs.weaviate.io/weaviate/model-providers) (OpenAI, Cohere, HuggingFace, and others) or direct import of [pre-computed vector embeddings](https://docs.weaviate.io/weaviate/starter-guides/custom-vectors). Production deployments benefit from built-in multi-tenancy, replication, RBAC authorization, and [many other features](https://github.com/weaviate/weaviate#weaviate-features).

To get started quickly, have a look at one of these tutorials:

- [Quickstart - Weaviate Cloud](https://docs.weaviate.io/weaviate/quickstart)
- [Quickstart - local Docker instance](https://docs.weaviate.io/weaviate/quickstart/local)

## Installation

Weaviate offers multiple installation and deployment options:
- [Docker](https://docs.weaviate.io/deploy/installation-guides/docker-installation)
- [Kubernetes](https://docs.weaviate.io/deploy/installation-guides/k8s-installation)
- [Weaviate Cloud](https://console.weaviate.cloud/)

See the [installation docs](https://docs.weaviate.io/deploy) for more deployment options, such as [AWS](https://docs.weaviate.io/deploy/installation-guides/aws-marketplace) and [GCP](https://docs.weaviate.io/deploy/installation-guides/gcp-marketplace).

```yaml
services:
  weaviate:
    image: cr.weaviate.io/semitechnologies/weaviate:1.32.2
    ports:
      - "8080:8080"
      - "50051:50051"
    environment:
      ENABLE_MODULES: text2vec-model2vec
      MODEL2VEC_INFERENCE_API: http://text2vec-model2vec:8080

  # A lightweight embedding model that will generate vectors from objects during import
  text2vec-model2vec:
    image: cr.weaviate.io/semitechnologies/model2vec-inference:minishlab-potion-base-32M
```

## ⚙️ How It Works

### 1️⃣ Store your data as vectors

You store data like documents, paragraphs, or images.  
Each gets converted into an **embedding vector** using an ML model (like OpenAI, Cohere, or Hugging Face).

```python
import weaviate
from weaviate.classes.config import Property, DataType

client = weaviate.connect_to_local()

client.collections.create(
    name="Articles",
    properties=[
        Property(name="title", data_type=DataType.TEXT),
        Property(name="content", data_type=DataType.TEXT),
    ]
)
```

### 2️⃣ Query by meaning

Instead of asking “exact keyword match,” you can ask:

> “Find articles about self-driving cars”

Weaviate uses vector similarity (cosine distance, dot product, etc.) to find the most semantically similar results.

```python
collection = client.collections.get("Articles")
result = collection.query.near_text("self-driving car safety", limit=5)
```

---

## 🧩 Core Features

|Feature|Description|
|---|---|
|🔢 **Vector search**|Find similar items by meaning (semantic search).|
|🧠 **Hybrid search**|Combine keyword (BM25) + vector search for best results.|
|🤖 **Integrations with AI models**|Works with OpenAI, Cohere, Hugging Face, etc. for embeddings.|
|🧱 **Modular architecture**|Choose your vectorizer or bring your own embeddings.|
|🔄 **RAG support**|Perfect backend for retrieval-augmented generation pipelines.|
|🌐 **REST & GraphQL APIs**|Query data easily from apps or Python clients.|
|☁️ **Fully managed or self-hosted**|Run locally (Docker/Kubernetes) or use Weaviate Cloud.|

---

## 🧮 Example: Semantic Search with Weaviate

```python
import weaviate
from weaviate.classes.init import Auth
from weaviate.embedded import EmbeddedOptions

# Connect to embedded/local instance
client = weaviate.Client(embedded_options=EmbeddedOptions())

collection = client.collections.get("Articles")
results = collection.query.near_text("climate change impact", limit=3)

for r in results.objects:
    print(r.properties["title"])
```

---

## ☁️ Deployment Options

- **Weaviate Cloud Service (WCS)** → fully managed by Weaviate
    
- **Self-hosted** → via Docker or Kubernetes
    
- **Embedded mode** → runs inside your Python app (great for local development)
    
---

## 🧰 Common Use Cases

|Use Case|Description|
|---|---|
|🔍 **Semantic Search**|Natural language search in your app|
|🧩 **RAG Pipelines**|Store embeddings and retrieve top-k context for LLMs|
|🗂️ **Knowledge Graphs**|Combine structured + unstructured data|
|🖼️ **Multimodal Search**|Search across text + image embeddings|
|🧠 **Clustering & Recommendations**|Find related content or items|

---

## 🔍 TL;DR

> **Weaviate** = a **vector database** for storing, searching, and retrieving embeddings — ideal for **AI, LLM, and RAG applications**.

---

Would you like me to show you a **minimal example of using Weaviate in a RAG pipeline** (embedding + retrieval + LLM prompt)?
# Note


# Reference
- [weaviate github](https://github.com/weaviate/weaviate)
- 


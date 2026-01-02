
Date: 2025-10-26
Course:
Tags: [[AI]] [[AI Agent]] [[Local]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content

**Ollama** has become a key player in the new generation of *local AI tooling*, especially if you’re a developer working with LLMs (Large Language Models). Let’s break it down in practical terms 👇
## 🧠 What Is **Ollama**
**Ollama** is a **local runtime and model manager** for running **large language models (LLMs)** **on your own computer** — similar to how Docker runs containers.
```sh
ollama pull open-soruce-model-name
# example
ollama pull llama3.2 # Facebook
ollama pull gpt-oss
```

➡️ **Official site:** [https://ollama.com](https://ollama.com)

You can think of it as:

> “A simple way to run and manage LLMs locally — like `llama3`, `mistral`, `phi`, or `gemma` — without needing to handle model weights, CUDA setup, or tokenizers manually.”

It provides:

* A **CLI tool** (`ollama run <model>`).
* A **local API server** (`localhost:11434`) for integration with apps.
* A **model registry** (like Docker Hub, but for models).

## ⚙️ How It Works

1. You install it on your machine:

   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. Pull and run a model:

   ```bash
   ollama run llama3
   ```

   This will:

   * Download the model (if not already cached).
   * Start it locally (using your CPU or GPU).
   * Give you an interactive chat shell.

3. Use it from code or tools (e.g., LangChain, OpenWebUI, local RAG apps):

   ```python
   import requests

   response = requests.post("http://localhost:11434/api/generate", json={
       "model": "llama3",
       "prompt": "Write a haiku about software engineers."
   })

   print(response.json()["response"])
   ```

So it’s essentially a **local inference server** for open-source LLMs.


## Simple example
```python
from ollama import Client

client = Client ()

resp = client.generate(
	model='llava:13b-v1.6',
	prompt='describe this image and make sure to include anything notable about it (include text you see in the image):',
	images=[image_bytes],
	stream=True
)

print(resp[0]['response'], end='', flush=True)
```
---

## 🧩 When You’d Want to Use Ollama

You’d use **Ollama** if you want to:
### ✅ 1. **Run models locally (no cloud or API cost)**

* Avoid using OpenAI, Anthropic, or Gemini APIs.
* Keep your data private (never leaves your machine).
* Experiment offline.

### ✅ 2. **Integrate open LLMs in your apps**

If you’re building:

* A **local chatbot**
* A **LangChain or LlamaIndex app**
* A **Retrieval-Augmented Generation (RAG)** system
* A **personal AI assistant** or **developer tool**

Then Ollama provides a clean, consistent local API to serve models.

### ✅ 3. **Switch between models easily**

For example:

```bash
ollama pull mistral
ollama run phi3
ollama run gemma2
```

No need to install PyTorch or transformers manually — Ollama handles model weights, tokenizers, and runtime.

### ✅ 4. **Run models in production (edge or on-prem)**

If your organization has privacy requirements, you can deploy Ollama on a private server (e.g., EC2, M1/M2 Mac, GPU machine) and serve models without sending data to external APIs.

---

## ⚡️ Features Summary

| Feature                  | Description                                                                 |
| ------------------------ | --------------------------------------------------------------------------- |
| **Local inference**      | Run models on your own hardware (CPU/GPU).                                  |
| **Supported models**     | LLaMA 3, Mistral, Gemma, Phi-3, Command R+, etc.                            |
| **Docker-like workflow** | `ollama pull`, `ollama run`, `ollama list`.                                 |
| **REST API**             | Exposes `http://localhost:11434/api` for apps.                              |
| **Model customization**  | Create your own `Modelfile` (like Dockerfile) to fine-tune or merge models. |
| **Cross-platform**       | macOS, Linux, and Windows (via WSL).                                        |

---

## 🧠 Example: Simple RAG Workflow with Ollama

If you’re building a local RAG system:

1. Use **ChromaDB** or **FAISS** to store embeddings.
2. Use **Ollama** as the local LLM:

   ```python
   from langchain.llms import Ollama

   llm = Ollama(model="mistral")
   llm("Summarize this article in 3 bullet points.")
   ```
3. Combine it with your local documents — fully private, no API fees.

---

## 🚀 When You *Shouldn’t* Use Ollama

Avoid Ollama if:

* You need **massive scale** (thousands of concurrent users).
* You require **very large models** (like GPT-4 or Claude 3) that exceed local GPU/CPU limits.
* You’re building a **cloud-native SaaS** that depends on guaranteed uptime.

For those cases, use **cloud-hosted APIs** (OpenAI, Anthropic, Bedrock, Vertex AI, etc.).

---

## 🧭 Summary

| Scenario                                      | Use Ollama?            |
| --------------------------------------------- | ---------------------- |
| Running local LLMs for privacy or cost saving | ✅ Yes                  |
| Experimenting with open-source models         | ✅ Yes                  |
| Building a local chatbot or RAG system        | ✅ Yes                  |
| Production-scale cloud deployment             | 🚫 No                  |
| Using GPT-4 / Claude / Gemini                 | 🚫 No (use their APIs) |

---

Would you like me to show you an example of **how to connect Ollama with LangChain** to build a local chat or RAG app (like a private ChatGPT clone)?

# Note


# Reference


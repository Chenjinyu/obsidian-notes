Date: 2025-10-26
Course:
Tags: [[ML]] [[LLM]] [[Base Knowledge]] [[Terminology]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content

## Foundation Model
### ✅ Definition: Foundation Model

A **foundation model** is a **large-scale machine learning model** trained on broad, diverse, and massive datasets using **self-supervised learning**, and then adapted (via fine-tuning or prompting) to a wide range of downstream tasks.

It is called a "foundation" model because:

* It serves as a **base** for many other applications.
* It captures **general knowledge** across domains (language, vision, code, etc.).
* It is designed to be **reusable and adaptable** across many use cases.

Examples:

* **GPT-4**, **Claude**, **LLaMA**, **PaLM** (language models)
* **CLIP**, **DINOv2** (vision-language models)
* **SAM** (Segment Anything Model, for segmentation)

### 🧠 Can *you* train a foundation model?

**Technically yes, but practically no**, unless you have:

* **Millions to tens of millions of dollars**
* Access to **thousands of GPUs or TPUs**
* **Petabytes** of curated training data
* Expertise in distributed training, optimization, and safety

**Why not feasible for most developers/teams?**

* Training GPT-3 cost millions and took weeks on a supercluster.
* It involves data pipelines, alignment/safety checks, evaluations, etc.

### ✅ What *you* can (and should) do instead:

1. **Fine-tuning** (full or parameter-efficient)

   * Train on your task-specific data using a pre-trained foundation model.
   * Methods: LoRA, PEFT, QLoRA, adapters, full fine-tuning.
   * Best for domain-specific tasks (e.g., legal, medical, customer support).

2. **Prompt engineering**

   * Use smart prompting or few-shot examples to guide the model.
   * Useful when data is small or you need fast results without retraining.

3. **RAG (Retrieval-Augmented Generation)**

   * Combine foundation models with your external knowledge base (e.g., vector DB).
   * Helps models answer accurately using up-to-date or domain-specific content.

### 🧩 Summary

| Term               | Description                                 | Can you do it?  |
| ------------------ | ------------------------------------------- | --------------- |
| Foundation Model   | Base large model trained on broad data      | ❌ Not practical |
| Fine-tuning        | Adapt model on your data/task               | ✅ Yes           |
| Prompt engineering | Guide behavior without changing model       | ✅ Yes           |
| RAG                | Add knowledge to model via external sources | ✅ Yes           |


The terms **foundation model** and **large language model (LLM)** are closely related but **not exactly the same**. Here's a breakdown of the key differences:

---

## Foundation models vs Large Language Models
### 🧠 1. **Scope and Definition**

| Term                           | Definition                                                                                                                                                          |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Foundation Model**           | A **broad category** of large models trained on massive data using self-supervised learning. They are adaptable to many downstream tasks (not limited to language). |
| **Large Language Model (LLM)** | A **subset** of foundation models that are trained specifically on **natural language** data. Their primary function is language understanding and generation.      |

### 🧰 2. **Modality**

| Feature      | Foundation Model                                                                     | LLM                                    |
| ------------ | ------------------------------------------------------------------------------------ | -------------------------------------- |
| **Modality** | Multimodal: can include **text, vision, audio, code** (e.g., CLIP, Flamingo, DALL·E) | Primarily **text**                     |
| **Examples** | GPT-4 (text), SAM (vision), DINOv2 (vision), Flamingo (vision+language)              | GPT-3, LLaMA, Claude, PaLM (text-only) |

### 🎯 3. **Use Case**

| Aspect          | Foundation Model                                                                                 | LLM                                                                                        |
| --------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| **General use** | Adaptable to **many domains** — image classification, captioning, segmentation, text, code, etc. | Primarily used for **language-based tasks** — Q\&A, summarization, translation, chat, etc. |
| **Examples**    | Use a foundation model for both visual segmentation and captioning                               | Use an LLM to summarize legal documents                                                    |

### 🔧 4. **Architecture**

| Point                          | Foundation Model                                                                           | LLM                                                                  |
| ------------------------------ | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| **Includes LLMs?**             | ✅ Yes — LLMs are part of foundation models                                                 | ❌ No — LLMs are narrower in scope                                    |
| **Examples of broader models** | Foundation models can be vision transformers, diffusion models, or multimodal transformers | LLMs are typically based on transformer architecture focused on text |

### 🧩 Summary Table

| Feature             | Foundation Model         | Large Language Model (LLM)  |
| ------------------- | ------------------------ | --------------------------- |
| Scope               | Broad, multi-domain      | Text-only                   |
| Modality            | Text, image, audio, code | Text                        |
| Example             | GPT-4, DALL·E, CLIP      | GPT-3, Claude, LLaMA        |
| LLM is a type of... | ✅ Foundation Model       | ❌ Not all foundation models |

---

Let me know if you want a diagram to visualize this!



# Note


# Reference


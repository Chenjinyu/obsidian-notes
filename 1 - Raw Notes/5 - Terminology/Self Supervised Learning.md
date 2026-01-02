Date: 2025-10-26
Course:
Tags: [[ML]] [[LLM]] [[Base Knowledge]] [[Terminology]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content

## Table of Contents
- [What Is Self-Supervised Learning (SSL)](#-what-is-self-supervised-learning-ssl)
- [Python Example](#python-example)

#### 🧠 What Is **Self-Supervised Learning (SSL)**?

**Self-supervised learning** is a type of machine learning that learns **representations or patterns from unlabeled data** by creating its **own learning signals** from the data itself — **without needing manual labels**.

It sits between **supervised** and **unsupervised** learning:

* Unlike supervised learning: **No need for human-labeled datasets**
* Unlike unsupervised learning: **It creates a task to learn something meaningful**, not just clustering or dimensionality reduction

#### 🔧 How It Works (Simple Explanation)

In self-supervised learning:

* The model is **given part of the data** and **tasked with predicting another part** of the same data.

##### 🔤 Examples:

| Domain     | Self-Supervised Task                                                       | What Model Learns                         |
| ---------- | -------------------------------------------------------------------------- | ----------------------------------------- |
| Text (NLP) | Mask part of a sentence (e.g., "I love \_\_") and predict the missing word | Language understanding (e.g., BERT)       |
| Images     | Predict the missing patch in an image                                      | Visual representation (e.g., SimCLR, MAE) |
| Audio      | Predict future audio frames from the past                                  | Speech features (e.g., wav2vec)           |
| Video      | Predict future frames or motion direction                                  | Temporal and spatial features             |

#### 🛠️ When to Use Self-Supervised Learning

You should consider **SSL** when:

| Situation                         | Why SSL Works Well                                                |
| --------------------------------- | ----------------------------------------------------------------- |
| ❌ No labeled data                 | SSL leverages **massive unlabeled datasets**                      |
| 🏗️ Pretraining needed            | Useful for **foundation models** or **transfer learning**         |
| 🧠 You want general understanding | Great for learning embeddings or **semantic representations**     |
| 💰 Labeling is too expensive      | Reduces cost of annotation, especially in healthcare, legal, etc. |

#### ✅ Examples in the Real World

| Area     | SSL Used In                          | Outcome                              |
| -------- | ------------------------------------ | ------------------------------------ |
| NLP      | BERT, GPT, RoBERTa                   | Pretrained language models           |
| Vision   | SimCLR, MAE, DINO                    | Vision transformers                  |
| Speech   | wav2vec, HuBERT                      | Robust speech recognition            |
| Robotics | Predicting actions from sensor input | Motion planning & control            |
| Finance  | Predicting missing transactions      | Fraud detection and account modeling |

#### 🧠 TL;DR

> **Self-supervised learning** is like giving a model a puzzle to solve using only the information in the data itself. It’s powerful when you have a **lot of unlabeled data** and want to **pretrain strong representations**.


---
 

## Python Example


We’ll use 🤗 **Hugging Face Transformers** with `bert-base-uncased`.

### 🧠 Self-Supervised NLP Example: Masked Word Prediction

#### 🧩 What it does:

1. Mask some words in a sentence.
2. Let the model predict the masked word based on the context.

#### ✅ Prerequisites:

Install Hugging Face packages if you haven’t:

```bash
pip install transformers torch
```

#### 🧪 Code Example:

```python
from transformers import BertTokenizer, BertForMaskedLM
import torch

# Load pre-trained BERT and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForMaskedLM.from_pretrained('bert-base-uncased')

# Example sentence with a [MASK]
text = "The capital of France is [MASK]."
inputs = tokenizer(text, return_tensors="pt")

# Get predictions
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits

# Find the index of the [MASK] token
mask_token_index = torch.where(inputs.input_ids == tokenizer.mask_token_id)[1]

# Get top 5 predicted tokens for the [MASK]
mask_logits = logits[0, mask_token_index, :]
top_5 = torch.topk(mask_logits, 5, dim=1)

for token_ids in top_5.indices[0]:
    word = tokenizer.decode([token_ids])
    print("Predicted:", word)
```

#### 💡 Output (example):

```
Predicted: paris
Predicted: france
Predicted: lyon
Predicted: rome
Predicted: berlin
```

The model has **learned language patterns** by masking parts of text and predicting them — without any manual labels. That's **self-supervised learning in action.**


# Note


# Reference


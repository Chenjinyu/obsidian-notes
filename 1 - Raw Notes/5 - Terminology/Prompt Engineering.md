Date: 2025-10-26
Course:
Tags: [[AI]] [[ML]] [[Base Knowledge]] [[Terminology]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content

## Table of Contents
- [What is the Prompt Engineering](#what-is-the-prompt-engineering)
- [TOP-K, TOP-P, and Temperature: What Are They?](#-top-k-top-p-and-temperature-what-are-they)
### What is the Prompt Engineering

**Prompt engineering** is the practice of **designing and refining input prompts** to guide large language models (LLMs) like GPT-4 to produce **more accurate, useful, or creative outputs**.

It’s essentially the **art and science of talking to AI effectively**.

#### 🛠️ Why Is It Important?

Because LLMs don’t *think* — they predict the next word based on your input. The **quality of the output heavily depends on how you ask**.

Just like asking a person:

> “Explain like I’m five” vs “Give a technical overview”
> produces totally different answers — same with LLMs.

#### 🧰 Core Techniques in Prompt Engineering

| Technique                      | Description                                               | Example                                                   |
| ------------------------------ | --------------------------------------------------------- | --------------------------------------------------------- |
| **Instruction Prompting**      | Clearly describe what you want                            | “Summarize the following article in 3 bullet points…”     |
| **Few-shot Prompting**         | Give a few input-output examples before your query        | Q: Paris is in which country? A: France...                |
| **Zero-shot Prompting**        | Just ask the question, no examples                        | “Translate this to Spanish: ‘Good morning’”               |
| **Chain-of-Thought Prompting** | Ask the model to explain reasoning step by step           | “Solve the math problem step by step: 23×12=”             |
| **Role Prompting**             | Ask the model to adopt a persona                          | “You are a senior software engineer. Review this code...” |
| **Context Augmentation**       | Provide background, context, or definitions in the prompt | “Based on the following company policy...”                |

#### 🧪 Real-World Example

```txt
Bad Prompt:
What’s the capital?

Good Prompt:
What’s the capital of Germany?
```

```txt
Bad Prompt:
Summarize this.

Good Prompt:
Summarize the following meeting transcript in 5 concise bullet points for a busy executive.
```

#### 💡 Where Prompt Engineering Is Used

| Area                      | Purpose                                              |
| ------------------------- | ---------------------------------------------------- |
| **Chatbots & Assistants** | Guide tone, role, and precision                      |
| **Coding Assistants**     | Generate code or fix bugs from detailed instructions |
| **Data Processing**       | Extract structured data from messy text              |
| **Creative Writing**      | Generate stories, poems, or jokes                    |
| **Business Intelligence** | Ask questions over documents, logs, or reports       |

#### 🧩 Summary

| Aspect            | Description                                              |
| ----------------- | -------------------------------------------------------- |
| **What**          | Crafting effective inputs for LLMs                       |
| **Why**           | To control and optimize output quality                   |
| **Used In**       | Chatbots, automation, content generation, coding, etc.   |
| **Skills Needed** | Clear thinking, communication, testing, domain knowledge |


---

### 🧠 **TOP-K, TOP-P, and Temperature: What Are They?**

These are **sampling parameters** used **during text generation**, not during model training.

| Parameter       | What It Does                                                                                                                  |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Top-K**       | Selects from the top **K most likely tokens** only (limits vocabulary).                                                       |
| **Top-P**       | Also known as **nucleus sampling**: chooses from the smallest set of tokens whose cumulative probability ≥ P.                 |
| **Temperature** | Controls randomness: lower = more deterministic, higher = more random. Affects the sharpness of the probability distribution. |

#### 🔁 **Used When?**

| Stage                                          | Can Use Top-K, Top-P, Temperature? | Purpose                                                                                                                                                |
| ---------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Prompting / Inference / Generation**         | ✅ Yes                              | To control the **style, creativity, and randomness** of responses.                                                                                     |
| **Model Training (Pretraining / Fine-tuning)** | ❌ No                               | These parameters are **not used during training**. Training uses **maximum likelihood estimation** or **loss functions** directly on token prediction. |

#### 🎨 **When Should You Use Each?**

| Scenario                                  | Recommended Setting                             |
| ----------------------------------------- | ----------------------------------------------- |
| **Creative writing / storytelling**       | Higher temperature (e.g., 0.8–1.0), Top-P (0.9) |
| **Code generation or QA**                 | Lower temperature (e.g., 0–0.3), Top-K or Top-P |
| **Deterministic output (same each time)** | Temperature = 0; disable Top-K/P                |
| **Balanced response**                     | Temperature = 0.7, Top-P = 0.9 (common default) |

#### 🔍 Visual Analogy

* **Temperature = 1.0** → Like rolling a weighted dice.
* **Top-K = 10** → Pick only from top 10 words.
* **Top-P = 0.9** → Pick from smallest group of words whose total prob ≥ 90%.

#### ✅ Summary

| Feature         | During Prompting | During Training |
| --------------- | ---------------- | --------------- |
| **Top-K**       | ✅ Yes            | ❌ No            |
| **Top-P**       | ✅ Yes            | ❌ No            |
| **Temperature** | ✅ Yes            | ❌ No            |

Use these when you're **generating text**, not when you're **training a model**.

Let me know if you'd like sample code or visual graphs!


# Note


# Reference


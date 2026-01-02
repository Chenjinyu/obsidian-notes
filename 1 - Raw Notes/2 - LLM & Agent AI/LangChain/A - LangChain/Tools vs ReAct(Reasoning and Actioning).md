Date: 2025-12-13
Course:
Tags: [[LangChain]] [[LLM]] [[AI Agent]] [[Backend]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content

### 1. LangChain Tools (The Capability)

- **What they are:** Tools in LangChain are simply **callable functions** with well-defined inputs and outputs (like a simple API wrapper) that an LLM-powered agent can invoke.
- **Purpose:** They extend the capabilities of the Large Language Model (LLM) beyond just generating text.
    - **Examples:** A `WebSearchTool` to fetch real-time data, a `CalculatorTool` to perform math, or a custom tool to query a database or API.
- **Role in AI:** They are the **action layer** that allows the agent to interact with the external world and access up-to-date information. The model decides when and how to call them.
### 2. ReAct (Reasoning and Acting)

- **What it is:** **ReAct** is a specific **prompting strategy and agent architecture** often implemented in LangChain. It stands for **Reasoning and Acting**.
- **Purpose:** It guides the LLM to follow an explicit, iterative **Thought → Action → Observation** loop until it reaches a final answer.
    - **Thought:** The agent narrates its reasoning for the next step.
    - **Action:** The agent decides which tool to call (a LangChain tool).
    - **Observation:** The agent receives the result from the executed tool, which is then fed back into the next step of the LLM's reasoning.
- **Key Feature:** This loop makes the agent's logic transparent, easier to debug, and capable of complex, multi-step problem-solving.

The ReAct should work with LangSimth to know and debug the process of Thought/Action
![[Pasted image 20251213225142.png]]
# Note


# Reference


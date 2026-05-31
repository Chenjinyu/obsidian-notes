
How to build an AI agent, like chat agent / eco-system agent
# Reference Links
### Stanford CS230 | Autumn 2025 | Lecture 8: Agents, Prompts, and RAG
Original Stanford Course on Youtube: https://www.youtube.com/watch?v=k1njvbBmfsw

### Stanford AI 系統課程，從 LLM 到 Agentic Workflow
Chinese version summary of the standard course: https://www.youtube.com/watch?v=eKW9ITaltWw

![](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260530025027484.png)

1. lack of domain knowledge
2. out of data of information. 
3. hard to control
4. Lost in the middle. when the context is too long.


## LLM
### 1. The Jagged Frontier（锯齿边界）, 
![400](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531015744092.png)
### 2. Falling Asleep at the Wheel
![400](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531015729773.png)

### 3. Centaurs vs Cyborgs
![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531015823762.png)
![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531015915433.png)

![](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531020011350.png)

![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531020049415.png)

Chaining, not only easy to debug one by one, and it improves the observability. 

## Fine-Tuning. 
![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531020232740.png)
![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531020257655.png)

## RAG
![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531020340000.png)

RAG chunk better choice: 
![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531020606830.png)

Long Context, cannot resolve the problem which RAG can provide:
1. Latency, every query needs to re-read the entire doc
2. RAG Index, prepare the answer. 
	1. could improve the accuracy
	2. improve query efficiency.
	3. Easy to keep the content update. 

![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531020916727.png)

## Agent workflow, created by Andrew Ng. 
Agent workflow = prompt + tools + 

![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531021105810.png)
![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531021234538.png)
Because AI easy to Fuzzy, so bring the AppealFeature
![](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531021305621.png)

# Agent
![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531021533562.png)
## #2 Content Management: is to giving the agent the correct information to agent in a right time

### Memory
![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531021939874.png)

## Tools
![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531021747564.png)


![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531021458396.png)

![](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531022101126.png)
![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531022132626.png)

![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531022215802.png)

![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531022238267.png)
![](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531022256622.png)
![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531022317272.png)

![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531022638505.png)

# Multi Agent
![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531022750949.png)


![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531022902427.png)

![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531022948982.png)

![800](assets/Beyond%20LLM%20-%20From%20LLM%20to%20Agentic%20Workflow/file-20260531023038413.png)
---
sr-due: 2026-10-12
sr-interval: 1
sr-ease: 2.5
---
Date: 2026-10-12
Course:
Tags: #MCP

# Content

MCP support is stateful, because it has natural conversation flow, and its also security and access control, because all of the 3rd party API  credentials will manage and control by the MCP, the LLM(robot/AI model) never sees API keys, tokens, connection, strings, internal URLs. (how can i grant the MCP access to LLM?)

![](assets/MCP%20Workflow%20+%20Architecture%20Design/file-20261012203047784.png)
LLM first discovers the available tools by calling tools/list from the MCP, understands their capabilities, and the decides which one to use.

![](assets/MCP%20Workflow%20+%20Architecture%20Design/file-20261012015546099.png)

![](assets/MCP%20Workflow%20+%20Architecture%20Design/file-20261012030517108.png)

# Note


# Reference


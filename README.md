# 🤖 AI_Agent_Langgraph

This project demonstrates the implementation of LangGraph, a framework for orchestrating multiple collaborative agents to handle complex queries. It features various specialized agents—Plan Agent, Tool Agent, Reflection Agent, Feedback Agent, and more—working together to decompose, solve, and refine user tasks.

When a user provides a high-level or open-ended query, the system intelligently splits it into subtasks and returns a detailed, refined response after iterative feedback and reflection.

---

## 🧰 Tech Stack

- LangGraph – Agent orchestration framework

- LangChain – LLM tooling and chain composition

- Gradio – Interactive chat interface

- Python – Core programming language

- Groq + LLaMA-3 – High-performance LLM backend
---
🧠 Agents Used
🧠 Plan Agent – Breaks down complex queries into subtasks

🔧 Tool Agent – Executes each subtask using available tools

🪄 Task Refiner – Improves clarity, order, or necessity of subtasks

✅ Feedback Agent – Evaluates & improves subtask results

🔍 Reflection Agent – Assesses overall coherence and quality

🏁 Output Agent – Aggregates and finalizes the response

---

## 🔍 Features
🧠 Multi-Agent Collaboration Loop:

- Plan Agent breaks down complex queries into smaller, manageable subtasks

- Tool Agent executes each subtask using external tools or LLMs

- Reflection Agent evaluates whether the response is complete and suggests new or improved subtasks if necessary

- Feedback Agent reviews each result for correctness, completeness, usefulness, and clarity

- Task Refiner removes duplicates, merges related tasks, and adds or prunes subtasks to streamline execution

- This feedback-reflection loop continues iteratively until all tasks are resolved with high quality

- Output Agent formats the final response in a clean and structured manner for the user

- 💬 Interactive and minimal Gradio UI for chat-like interactions

- ⚡ Fast and accurate responses powered by Groq Cloud (LLaMA-3) backend
---
🌐 Live Demo
https://huggingface.co/spaces/hrry121/AI_Agent_Langgraph

## 🚀 Getting Started (Optional)

You can include a basic setup guide like:
```bash
git clone https://github.com/hrry121/AI_Agent_Langgraph.git

---
Install Requirements
```bash
pip install -r requirements.txt

---
Note make sure you have made .env file to keep your secret API keys

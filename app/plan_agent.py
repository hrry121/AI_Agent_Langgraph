import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

load_dotenv()

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY")
)

template = PromptTemplate.from_template("""
You are a planner agent. Break the following user query into clear sub-tasks.

Query: {query}

Return them as a numbered list.
""")

def plan_agent(state: dict):
    query = state["query"]
    prompt = template.format(query=query)
    response = llm.invoke(prompt)

    # 👇 DEBUG: Show LLM raw response
    print("LLM Response:\n", response.content)

    subtasks = []
    for line in response.content.splitlines():
        line = line.strip("-* \t")
        if not line or line.lower().startswith("here are") or line.lower().startswith("these sub-tasks"):
           continue
        if line[0].isdigit() and "." in line:
           subtasks.append(line)
        elif subtasks:
           subtasks[-1] += " " + line



    return {
        "query": query,
        "subtasks": subtasks,
        "step": 0,
        "results": []
    }

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import re

load_dotenv()

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.4,
    api_key=os.getenv("GROQ_API_KEY")
)

template = PromptTemplate.from_template("""
You are an expert refiner. Given the following list of subtasks, improve them by:
- Merging duplicates
- Removing unnecessary ones
- Adding new task if necessary

Subtasks:
{subtasks}

Return the cleaned list as bullet points or numbered list. No need for unnecessary content
""")

def task_refiner(state: dict):
    subtasks = "\n".join(f"- {task}" for task in state["subtasks"])
    prompt = template.format(subtasks=subtasks)
    response = llm.invoke(prompt)

    print("\n🔁 Refined LLM Response:\n", response.content)

    # Support both bullet points and numbered list
    lines = response.content.splitlines()
    state["subtasks"] = [
        re.sub(r"^[\-\d\.\)\s]+", "", line).strip()
        for line in lines
        if line.strip()
    ]

    print("✅ Parsed Subtasks:\n", state["subtasks"])
    return state

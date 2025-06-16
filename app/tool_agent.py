import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

load_dotenv()

llm = ChatGroq(
    model_name="llama3-8b-8192",
    temperature=0.4,
    api_key=os.getenv("GROQ_API_KEY")
)

template = PromptTemplate.from_template("""
You are like Chatgpt. Execute the following subtask and return a concise and on point result like any human expects.

Subtask: {subtask}
""")

def tool_agent(state: dict) -> str:
    step = state["step"]
    subtask = state["subtasks"][step]

    print(f"🔧 Executing Subtask {step + 1}: {subtask}")

    prompt = template.format(subtask=subtask)
    response = llm.invoke(prompt)

    return response.content.strip()

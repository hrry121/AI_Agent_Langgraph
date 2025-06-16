import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableMap
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

# LLM instance
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.4,
    api_key=os.getenv("GROQ_API_KEY")
)

# Prompt template
reflection_prompt = PromptTemplate.from_template("""
You are a Reflective Agent.

Original user query:
{query}

Results from executed subtasks:
{results}

Evaluate the following:
1. Are the results complete and useful in answering the original query?
2. Were any important subtasks missed or poorly addressed?
3. Suggest improvements or new subtasks if needed.
4. If no improvements are needed, clearly say "The results are sufficient."

🧠 Reflection:
""")

# Chain setup
parser = StrOutputParser()
ReflectionAgent: Runnable = RunnableMap({
    "reflection": reflection_prompt | llm | parser
}).with_config({"run_name": "ReflectionAgent"})


# Function to run reflection agent and parse output
def reflection_agent(state: dict) -> dict:
    # Format results into bullet points
    formatted_results = "\n".join([
        f"{i + 1}. {res.strip()}" for i, res in enumerate(state.get("results", []))
    ])

    inputs = {
        "query": state.get("query", "N/A"),
        "results": formatted_results
    }

    try:
        response = ReflectionAgent.invoke(inputs)
        raw_reflection = response["reflection"].strip()
        print("\n🧠 Raw Reflection Output:\n", raw_reflection)

        # Simple parsing strategy
        result = {
            "status": "pass" if "sufficient" in raw_reflection.lower() else "refine",
            "reason": raw_reflection,
            "confidence": 0.8,  # Static for now
            "suggested_subtasks": [],
            "modifications": [],
            "missing_aspects": []
        }

        # Extract optional actionable suggestions if any
        if "suggest" in raw_reflection.lower() or "new subtasks" in raw_reflection.lower():
            lines = raw_reflection.split("\n")
            for line in lines:
                if line.strip().startswith("-"):
                    result["suggested_subtasks"].append(line.strip("- ").strip())

        return result

    except Exception as e:
        print("⚠️ Reflection Agent Error:", e)
        return {
            "status": "error",
            "reason": str(e),
            "suggested_subtasks": [],
            "modifications": [],
            "missing_aspects": []
        }

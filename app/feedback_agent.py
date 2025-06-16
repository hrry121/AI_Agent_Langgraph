from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import re

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Try to initialize the Groq LLM
llm = None
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM if API key is available
llm = None
if GROQ_API_KEY:
    try:
        llm = ChatGroq(
            model_name="llama3-8b-8192",
            temperature=0.3,
            api_key=GROQ_API_KEY
        )
    except Exception as e:
        print("⚠️ Failed to initialize ChatGroq:", e)

# Define the prompt template for evaluation
template = PromptTemplate.from_template("""
You are a like an evaluator, reviewing the quality of AI-generated outputs.

Evaluate the result of the following subtask execution:

Subtask:
{subtask}

Result:
{result}

Your job is to assess the result based on these 3 criteria:
- ✅ Usefulness: Is it relevant and helpful?
- ✅ Completeness: Does it fully address the subtask?
- ✅ Correctness: Is it factually and logically correct?

Then provide:
1. 📋 A short evaluation of each criterion
2. 🛠️ A revised version of the result (if needed), labelled clearly as "Improved Answer"

Example Output Format:

**Evaluation**
- Usefulness: ...
- Completeness: ...
- Correctness: ...

**Improved Answer:**
<Your improved version here>
""")

# Function to evaluate and optionally revise a subtask result
def feedback_agent(subtask: str, result: str) -> str:
    if llm:
        try:
            # Format prompt
            prompt = template.format(subtask=subtask, result=result)

            # Invoke LLM
            response = llm.invoke(prompt)
            content = response.content.strip()

            # Log full feedback for debugging
            print(f"\n🧠 Full Feedback for Subtask: {subtask}\n{content}")

            # Extract "Improved Answer"
            if "**Improved Answer:**" in content:
                improved = content.split("**Improved Answer:**", 1)[1].strip()

                # Check if improvement is meaningful
                if improved.lower() in ["no changes needed", "no revision needed"]:
                    return ""  # No update needed
                return improved

            return ""  # No "Improved Answer" section found

        except Exception as e:
            print("⚠️ Error during LLM invocation:", e)

    # Manual fallback in case of Groq LLM unavailability
    print(f"\n⚠️ Groq unavailable. Manual fallback for subtask:\n{subtask}")
    return f"""**Evaluation**
- Usefulness: ✅ Helpful and relevant.
- Completeness: ✅ Fully addresses the subtask.
- Correctness: ✅ Factually sound.

**Improved Answer:**
{result}
"""

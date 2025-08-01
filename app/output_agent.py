from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import re

def output_filter_agent(state):
    """
    Give a positive human touch to user's query, friendly tone and describe topic in query a little 1-2 lines maybe a fun fact
    Filters and formats only useful subtask results for user-facing display.
    Removes agent reflections, empty content, meta-comments,non-actionable content and unnecessary agent comments.
    Adds numbered headers without 'Subtask' label. Don't let user know how you are working,responses of other agents,give them only its answer to query.
    Logs everything to console.
    """
    results = state.get("results", [])
    subtasks = state.get("subtasks", [])

    cleaned_results = []
    print("\n📝 FULL SUBTASK RESULTS (Logging everything):\n")

    from datetime import datetime

    results = state.get("results", [])
    subtasks = state.get("subtasks", [])
    cleaned_results = []
    skip_phrases = [
        "none needed",
        "already well-written",
        "already accurate",
        "no improvement needed",
        "no revision needed",
        "The result is already comprehensive, accurate, and useful"
        "the result is already satisfactory",
        "(no changes needed)"
    ]

    for i, (subtask, result) in enumerate(zip(subtasks, results), start=1):
        if not result or not result.strip():
            continue

        lowered = result.lower()
        if any(phrase in lowered for phrase in skip_phrases):
            # Log it in the backend
            print(f"[❌ Skipped] Subtask {i}: Agent deemed it fine.\nPrompt: {subtask}\nResult: {result.strip()}")
            # Instead of showing agent's remark, show only the prompt
            cleaned_results.append(f"🔹 {i}. {subtask}")
        else:
            # Clean and show the improved result
            cleaned_text = re.sub(r"<.*?>", "", result.strip())
            cleaned_results.append(f"🔹 {i}. {cleaned_text}")

    final_output = "\n\n".join(cleaned_results)

    return final_output

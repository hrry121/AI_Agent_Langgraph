
from app.output_agent import output_filter_agent
from app.plan_agent import plan_agent
from app.task_refiner import task_refiner
from app.tool_agent import tool_agent
from app.feedback_agent import feedback_agent
from app.reflection_agent import reflection_agent
import gradio as gr


def run_agent_ui(query: str):
    yield "🧠 Great Question, Give me a min ..."

    # PLAN AGENT
    state = plan_agent({"query": query})
    print("\n[🧠 Plan Agent] Initial Subtasks:")
    for sub in state["subtasks"]:
        print("   -", sub)

    # TASK REFINER
    state = task_refiner(state)
    print("\n[🧹 Task Refiner] Refined Subtasks:")
    for sub in state["subtasks"]:
        print("   -", sub)

    max_iterations = 1
    current_iteration = 0

    while current_iteration < max_iterations:
        print(f"\n[🔁 Iteration {current_iteration + 1}] Starting...")
        yield f"🔄 Iteration {current_iteration + 1} in progress..."

        state["step"] = 0
        state["results"] = []

        for idx, subtask in enumerate(state["subtasks"]):
            try:
                print(f"\n[🔧 Tool Agent] Subtask {idx + 1}: {subtask}")
                state["step"] = idx
                result = tool_agent(state)
                print(f"[✅ Tool Agent] Result:\n{result}")
                state["results"].append(result)
                yield f"Thinking..."

                # Feedback Agent
                improved_result = feedback_agent(subtask, result)
                if improved_result and improved_result.strip() != result.strip():
                    print(f"[✅ Feedback Agent] Improved Result:\n{improved_result}")
                    state["results"][-1] = improved_result
                else:
                    print("[✅ Feedback Agent] No improvement needed.")
            except Exception as e:
                print(f"[⚠️ Error] Subtask {idx + 1}: {e}")
                state["results"].append(f"(error on this subtask) {str(e)}")
                yield f"⚠️ Subtask {idx + 1} had an error."
        current_iteration += 1


    # Final Output
    yield "📌 Finalizing Output..."
    final_output = output_filter_agent(state)  # uses your cleaned/numbered output
    print("\n📌 FINAL OUTPUT:\n", final_output)

    yield f"✅ **Final Answer:**\n\n{final_output}"

gr.Interface(
    fn=run_agent_ui,
    inputs=gr.Textbox(
        label="💬 What would you like help with?",
        placeholder="e.g.Create a startup plan for an AI app, Plan a vacation ...",
        lines=3
    ),
    outputs=gr.Markdown(label="🤖 Agent Response"),
    title="LangGraph Agent Workspace",
    description="🤖 Ask complex queries and watch the LangGraph agents collaborate.",
    allow_flagging="never",
    theme="soft"
).launch()

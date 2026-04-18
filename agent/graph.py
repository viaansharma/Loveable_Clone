from dotenv import load_dotenv
from langchain.agents import create_agent
# Change this import
from langchain_core.globals import set_verbose, set_debug

from langchain_groq.chat_models import ChatGroq
from langgraph.constants import END

from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent

from agent.prompts import *
from agent.states import *
from agent.tools import write_file, read_file, get_current_directory, list_files, init_project_root

_ = load_dotenv()

set_debug(True)
set_verbose(True)

#llm = ChatGroq(model="openai/gpt-oss-120b")

# Switch to a more robust model for complex structured outputs
llm = ChatGroq(model="openai/gpt-oss-120b")

def planner_agent(state: dict) -> dict:
    user_prompt = state["user_prompt"]
    resp = llm.with_structured_output(Plan).invoke(
        planner_prompt(user_prompt)
    )
    if resp is None:
        raise ValueError("Planner did not return a valid response.")
    return {"plan": resp}


# def architect_agent(state: dict) -> dict:
#     plan: Plan = state["plan"]
#     resp = llm.with_structured_output(TaskPlan).invoke(
#         architect_prompt(plan=plan.model_dump_json())
#     )
#     if resp is None:
#         raise ValueError("Architect did not return a valid response.")
#
#     resp.plan = plan
#     return {"task_plan": resp}

def architect_agent(state: dict) -> dict:
    plan: Plan = state["plan"]
    # Instead of model_dump_json(), provide a clean string summary
    # This prevents 'JSON-inside-JSON' parsing errors later
    plan_summary = (
        f"App Name: {plan.name}\n"
        f"Stack: {plan.techstack}\n"
        f"Files to create: {[f.path for f in plan.files]}"
    )

    resp = llm.with_structured_output(TaskPlan).invoke(
        architect_prompt(plan=plan_summary)
    )
    if resp is None:
        raise ValueError("Architect failed.")

    resp.plan = plan
    return {"task_plan": resp}



# def coder_agent(state: dict) -> dict:
#     # Safely get or initialize coder_state
#     coder_state = state.get("coder_state")
#     if coder_state is None:
#         coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)
#
#     steps = coder_state.task_plan.implementation_steps
#
#     # Check if we are finished
#     if coder_state.current_step_idx >= len(steps):
#         return {"status": "DONE"}
#
#     current_task = steps[coder_state.current_step_idx]
#
#     # Pre-read the file if it exists
#     existing_content = read_file.run(current_task.filepath)
#
#     system_prompt = coder_system_prompt()
#     user_task_msg = (
#         f"Task: {current_task.task_description}\n"
#         f"File: {current_task.filepath}\n"
#         f"Existing content:\n{existing_content}\n"
#         "Use write_file to save changes."
#     )
#
#     coder_tools = [read_file, write_file, list_files, get_current_directory]
#     react_agent = create_react_agent(llm, coder_tools)
#
#     # Execute the tool-calling agent
#     react_agent.invoke({"messages": [
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": user_task_msg}
#     ]})
#
#     # Increment index for the next node hit
#     coder_state.current_step_idx += 1
#
#     return {"coder_state": coder_state, "status": "CONTINUE"}

def coder_agent(state: dict) -> dict:
    """LangGraph tool-using coder agent."""
    # 1. Safely get or initialize coder_state
    coder_state = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)

    steps = coder_state.task_plan.implementation_steps

    # 2. Check if we have processed all steps
    if coder_state.current_step_idx >= len(steps):
        return {"status": "DONE", "coder_state": coder_state}

    current_task = steps[coder_state.current_step_idx]

    # 3. Handle file reading and empty states
    try:
        existing_content = read_file.invoke({"path": current_task.filepath})
    except Exception:
        existing_content = ""

    if not existing_content or existing_content.strip() == "":
        existing_content = "(File is currently empty or does not exist)"

    # 4. Construct a clear, structured prompt for the sub-agent
    system_prompt = coder_system_prompt()
    user_task_msg = (
        f"IMPLEMENTATION TASK:\n{current_task.task_description}\n\n"
        f"TARGET FILE: {current_task.filepath}\n\n"
        f"EXISTING CONTENT:\n{existing_content}\n\n"
        "CRITICAL INSTRUCTIONS:\n"
        "1. Use 'write_file' to save the complete updated code.\n"
        "2. Do not use backslashes in your reasoning that might break JSON parsing.\n"
        "3. Provide the FULL file content in the tool call."
    )

    # 5. Initialize the ReAct agent with specific tools
    coder_tools = [read_file, write_file, list_files, get_current_directory]
    react_agent = create_agent(llm, coder_tools)

    # 6. Execute the sub-agent
    # Note: We use invoke here; the sub-agent handles the tool loop internally
    react_agent.invoke({
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_task_msg}
        ]
    })

    # 7. Update progress and return
    coder_state.current_step_idx += 1

    # Print progress to console
    print(f"--- Finished Step {coder_state.current_step_idx} of {len(steps)} ---")

    return {"coder_state": coder_state, "status": "CONTINUE"}


# Initialize Graph
graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")

# Fixed conditional edge mapping
graph.add_conditional_edges(
    "coder",
    lambda s: s.get("status"),
    {
        "DONE": END,
        "CONTINUE": "coder"
    }
)

graph.set_entry_point("planner")
agent = graph.compile()

if __name__ == "__main__":
    init_project_root()  # Ensure the directory exists before running
    result = agent.invoke(
        {"user_prompt": "Build a colourful modern todo app in html css and js"},
        {"recursion_limit": 100}
    )
    print("Final State:", result)
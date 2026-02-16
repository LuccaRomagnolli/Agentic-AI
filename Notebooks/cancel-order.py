import os
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from langchain_core.tools import tool
from typing import TypedDict, List, Dict, Any

# Set your API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

# Define the state schema (structured output)
class State(TypedDict):
    order: Dict[str, Any]
    messages: List[Any]

# - Business tool
@tool
def cancel_order(order_id: str) -> str:
    """Cancel a order that hasn't shipped"""
    return f"Order {order_id} has been cancelled"

# - Invoke LLM, use tool and invoke LLM again (Agent Brain)
def call_model(state):
    msgs = state["messages"]
    order = state.get("order", {"order_id": "UNKNOWN"})

    # System prompt tells the model exactly what to do
    prompt = (
        f'''You are an ecommerce support agent.
ORDER ID: {order['order_id']}
If the customer asks to cancel, call cancel_order(order_id)
and then send a simple confirmation.
Otherwise, just respond normally.'''
    )

    full = [SystemMessage(prompt)] + msgs

    # 1st LLM pass: decides whether to call our tool
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    llm_with_tools = llm.bind_tools([cancel_order])
    first = llm_with_tools.invoke(full)
    out = [first]

    if getattr(first, "tool_calls", None):
        # run the cancel_order tool
        tc = first.tool_calls[0]
        result = cancel_order.invoke(tc["args"])

        out.append(ToolMessage(content=result, tool_call_id=tc["id"]))
        # 2nd LLM pass: generate the final confirmation text
        second = llm.invoke(full + out)
        out.append(second)

    return {"messages": out}

# -- 3) Wire it all up in a StateGraph
def construct_graph():
    g = StateGraph(State)
    g.add_node("assistant", call_model)
    g.set_entry_point("assistant")
    g.set_finish_point("assistant")
    return g.compile()

graph = construct_graph()

if __name__ == "__main__":
    example_order = {"order_id": "A12345"}
    convo = [HumanMessage(content="Please cancel my order A12345.")]
    result = graph.invoke({"order": example_order, "messages": convo})
    for msg in result["messages"]:
        print(f"{msg.type}: {msg.content}")

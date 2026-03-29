from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.messages.tool import ToolMessage
from langgraph.graph import StateGraph
from typing import TypedDict, List
from langchain_core.messages import BaseMessage
from load_api import load_models

class State(TypedDict):
    order: dict
    messages: List[BaseMessage]

@tool
def cancel_order(order_id: str) -> str:
  """Cancel an order that hasn't shipped."""
  # (Here you'd call your real backend API)
  return f"Order {order_id} has been cancelled."

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
 llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=load_models("gemini")).bind_tools([cancel_order])
 
 first = llm.invoke(full)
 out = [first]
 if getattr(first, "tool_calls", None):
    # run the cancel_order tool
    tc = first.tool_calls[0]
    result = cancel_order.invoke(tc["args"])
    out.append(AIMessage(content="Cancelling your order..."))
    out.append(ToolMessage(content=result, tool_call_id=tc["id"]))
    # 2nd LLM pass: generate the final confirmation text
    second = llm.invoke(full + out)
    out.append(second)
 return {"messages": out}
def construct_graph():
    g = StateGraph(State)
    g.add_node("assistant", call_model)
    g.set_entry_point("assistant")
    return g.compile()

graph = construct_graph()


if __name__ == "__main__":
    example_order = {"order_id": "A12345"}
    convo = [HumanMessage(content="Please cancel my order A12345.")]
    result = graph.invoke({"order": example_order, "messages": convo})
    for msg in result["messages"]:
        print(f"{msg.type}: {msg.content}") 
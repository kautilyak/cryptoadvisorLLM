import os

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv

from app.graph.nodes.categories import get_categories_with_changes
from app.graph.state import InputState, OutputState, OverallState
from app.graph.viz import mermaid


load_dotenv("../.env")
llm = ChatOpenAI(model="gpt-4o", temperature=0.5,
                 api_key=os.environ['OPENAI_API_KEY'])
llm_with_tools = llm.bind_tools([get_categories_with_changes])

system_message = SystemMessage(content="You are a helpful crypto investment advisor tasked at using the tools on hand "
                                       "to fetch relevant information and analyze it and advise on the profitability "
                                       "for buying a cryptocurrency.")


# Node
def tool_calling_llm(state: InputState):
    return {"messages": [llm_with_tools.invoke([system_message] + state["messages"])]}


# Construct an agent graph (ReAct)
graph = StateGraph(input=InputState, output=OutputState, state_schema=OverallState)
graph.add_node("advisor", tool_calling_llm)
graph.add_node("tools", ToolNode([get_categories_with_changes], messages_key="messages"))
graph.add_edge(START, "advisor")
graph.add_conditional_edges("advisor", tools_condition, {"tools": "tools", END: END})
graph.add_edge("tools", "advisor")

agent = graph.compile()

mermaid.visualize(agent)
# display(Image(agent.get_graph(xray=True).draw_mermaid_png()))

import os

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv

from app.graph.nodes.categories import get_categories_with_changes
from app.graph.state import OverallState
from app.viz import mermaid
import time


load_dotenv("../.env")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5,
                 api_key=os.environ['OPENAI_API_KEY'])
print(os.environ['OPENAI_API_KEY'])
llm_with_tools = llm.bind_tools([get_categories_with_changes])

system_message = SystemMessage(content="You are a helpful crypto investment advisor tasked at using the tools on hand "
                                       "to fetch relevant information and analyze it and advise on the profitability "
                                       "for buying a cryptocurrency.")


# Node
def advisor(state: OverallState):
    # Invoke the LLM with the tools
    result = llm_with_tools.invoke([system_message] + state["messages"])
    state["messages"].append(result)
    return state


# Construct an agent graph (ReAct)

graph = StateGraph(state_schema=OverallState)
graph.add_node("advisor", advisor)
graph.add_node("tools", ToolNode([get_categories_with_changes], messages_key="messages"))
graph.add_edge(START, "advisor")
graph.add_conditional_edges("advisor", tools_condition)
graph.add_edge("tools", "advisor")

agent = graph.compile()

config = {"configurable": {"thread_id": "1"}}

#pprint(len(get_categories_with_changes()))
# for step in agent.stream({"messages": "Find out all the categories of cryptocurrencies and give me a summary for the top 5 most traded by volume today."}, config=config, stream_mode="updates"):
#     print(f"{step}\n\n----------------\n")
#     time.sleep(5)

res = agent.invoke({"messages": "Find out all the categories of cryptocurrencies and give me a summary for the top 5 most traded by volume today."}, config=config)
print(res)

mermaid.visualize(agent)

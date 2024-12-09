from typing_extensions import TypedDict
from typing_extensions import Annotated, Any
from langgraph.graph import MessagesState
from typing import List, Dict


# Define the overall schema, combining both input and output
class OverallState(MessagesState):
    categories: List[Dict]


class CategoryAnalysisOutputState(TypedDict):
    categories: List[Dict]

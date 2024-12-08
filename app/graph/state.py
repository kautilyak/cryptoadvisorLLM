from typing_extensions import TypedDict
from typing_extensions import Annotated
from langgraph.graph import MessagesState


# Define a schema for the Input
class InputState(MessagesState):
    task: str


# Define a schema for the output
class OutputState(MessagesState):
    analysis: str


# Define the overall schema, combining both input and output
class OverallState(MessagesState):
    pass

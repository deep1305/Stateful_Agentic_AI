from typing_extensions import TypedDict, Annotated, NotRequired
from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    Represents the structure of the state used in the graph.
    """
    messages: Annotated[list, add_messages]
    query: NotRequired[str]
    frequency: NotRequired[str]
    news_data: NotRequired[list]
    summary: NotRequired[str]

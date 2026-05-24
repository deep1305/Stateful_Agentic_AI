import os

from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools(tavily_api_key=None):
    """
    Return the list of tools to be used in the chatbot
    """
    api_key = tavily_api_key or os.environ.get("TAVILY_API_KEY")
    if not api_key:
        raise ValueError(
            "Tavily API key is required. Enter it in the sidebar or set TAVILY_API_KEY."
        )

    tools=[TavilySearchResults(max_results=4, tavily_api_key=api_key)]
    return tools
def create_tool_node(tools):
    """
    creates and returns a tool node for the graph
    """
    return ToolNode(tools=tools)


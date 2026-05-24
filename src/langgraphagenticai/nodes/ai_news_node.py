import os
import re

from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate


class AINewsNode:
    def __init__(self, llm, tavily_api_key=None):
        """
        Initialize the AINewsNode with API keys for Tavily and the LLM.
        """
        api_key = tavily_api_key or os.environ.get("TAVILY_API_KEY")
        self.tavily = TavilyClient(api_key=api_key)
        self.llm = llm
        self.state = {}

    def fetch_news(self, state: dict) -> dict:
        """
        Fetch news based on the user query and selected frequency.
        """
        query = state.get("query", "").strip()
        frequency = state.get("frequency", "daily").lower()

        if not query:
            raise ValueError("Search query is required.")

        self.state["query"] = query
        self.state["frequency"] = frequency
        state["query"] = query
        state["frequency"] = frequency

        time_range_map = {"daily": "d", "weekly": "w", "monthly": "m", "year": "y"}
        days_map = {"daily": 1, "weekly": 7, "monthly": 30, "year": 366}

        response = self.tavily.search(
            query=query,
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=20,
            days=days_map[frequency],
        )

        state["news_data"] = response.get("results", [])
        self.state["news_data"] = state["news_data"]
        return state

    def summarize_news(self, state: dict) -> dict:
        """
        Summarize the fetched news using an LLM.
        """
        news_items = self.state["news_data"]
        query = self.state["query"]

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Summarize news articles into markdown format for the user's query.
            For each item include:
            - Date in **YYYY-MM-DD** format in IST timezone
            - Concise sentences summary from latest news
            - Sort news by date wise (latest first)
            - Source URL as link
            Use format:
            ### [Date]
            - [Summary](URL)"""),
            ("user", "Query: {query}\n\nArticles:\n{articles}"),
        ])

        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])

        response = self.llm.invoke(prompt_template.format(query=query, articles=articles_str))
        state["summary"] = response.content
        self.state["summary"] = state["summary"]
        return state

    def save_result(self, state):
        frequency = self.state["frequency"]
        query = self.state["query"]
        summary = self.state["summary"]
        safe_query = re.sub(r"[^\w\-]+", "_", query.lower())[:50]
        filename = f"./AINews/{frequency}_{safe_query}_summary.md"

        os.makedirs("./AINews", exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {frequency.capitalize()} News Summary\n\n")
            f.write(f"**Query:** {query}\n\n")
            f.write(summary)

        state["filename"] = filename
        self.state["filename"] = filename
        return state

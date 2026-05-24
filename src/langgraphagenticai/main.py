import streamlit as st

from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.LLMS.ollamallm import OllamaLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit


def _initialize_llm(user_input):
    selected_llm = user_input.get("selected_llm")

    if selected_llm == "Groq":
        return GroqLLM(user_contols_input=user_input).get_llm_model()
    if selected_llm == "Ollama":
        return OllamaLLM(user_contols_input=user_input).get_llm_model()

    st.error(f"Error: Unsupported LLM provider '{selected_llm}'.")
    return None


def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    """
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return

    usecase = user_input.get("selected_usecase")
    tavily_api_key = user_input.get("TAVILY_API_KEY") or st.session_state.get("TAVILY_API_KEY")

    if usecase == "AI News Summarizer" and st.session_state.get("IsFetchButtonClicked"):
        st.session_state.IsFetchButtonClicked = False

        news_query = user_input.get("news_query") or st.session_state.get("news_query", "")
        time_frame = user_input.get("time_frame") or st.session_state.get("time_frame", "Daily")

        if not tavily_api_key:
            st.error("Error: Please enter your TAVILY API key for this use case.")
            return

        if not news_query.strip():
            st.error("Error: Please enter a search query.")
            return

        try:
            model = _initialize_llm(user_input)
            if not model:
                return

            graph_builder = GraphBuilder(model, tavily_api_key=tavily_api_key)
            graph = graph_builder.setup_graph(usecase)

            initial_state = {
                "messages": [],
                "query": news_query.strip(),
                "frequency": time_frame.lower(),
            }

            DisplayResultStreamlit(usecase, graph, initial_state).display_result_on_ui()
        except Exception as e:
            st.error(f"Error: Graph execution failed- {e}")
        return

    user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            model = _initialize_llm(user_input)
            if not model:
                return

            if not usecase:
                st.error("Error: No use case selected.")
                return

            if usecase in ("Chatbot with Web Search", "AI News Summarizer") and not tavily_api_key:
                st.error("Error: Please enter your TAVILY API key for this use case.")
                return

            graph_builder = GraphBuilder(model, tavily_api_key=tavily_api_key)
            graph = graph_builder.setup_graph(usecase)
            DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()
        except Exception as e:
            st.error(f"Error: Graph set up failed- {e}")

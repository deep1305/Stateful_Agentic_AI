import streamlit as st

from src.langgraphagenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config=Config()
        self.user_controls={}

    def load_streamlit_ui(self):
        st.set_page_config(page_title= "🤖 " + self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())


        with st.sidebar:
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)
            selected_llm = self.user_controls["selected_llm"]

            if selected_llm == 'Groq':
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API Key", type="password")
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")

            elif selected_llm == 'Ollama':
                model_options = self.config.get_ollama_model_options()
                self.user_controls["selected_ollama_model"] = st.selectbox("Select Model", model_options)

            self.user_controls["selected_usecase"] = st.selectbox("Select Usecases", usecase_options)
            if self.user_controls["selected_usecase"] == "Chatbot with Web Search" or self.user_controls["selected_usecase"] == "AI News Summarizer":
                self.user_controls["TAVILY_API_KEY"] = st.text_input(
                    "TAVILY API Key",
                    type="password",
                    key="TAVILY_API_KEY",
                )
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("⚠️ Please enter your TAVILY API key to proceed. Don't have? refer : https://app.tavily.com/home")
            
            if self.user_controls["selected_usecase"] == "AI News Summarizer":
                st.subheader("📰 AI News Summarizer")

                self.user_controls["news_query"] = st.text_input(
                    "Enter search query",
                    placeholder="e.g. Latest AI startups in India",
                    key="news_query",
                )

                self.user_controls["time_frame"] = st.selectbox(
                    "⏰ Select Time Frame",
                    ["Daily", "Weekly", "Monthly"],
                    index=0,
                    key="time_frame",
                )

                if st.button("🔍 Fetch & Summarize News", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
        
        return self.user_controls
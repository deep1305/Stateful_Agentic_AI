import streamlit as st
from langchain_ollama import ChatOllama

class OllamaLLM:
    def __init__(self,user_contols_input):
        self.user_controls_input=user_contols_input

    def get_llm_model(self):
        try:
            selected_ollama_model=self.user_controls_input["selected_ollama_model"]
            if selected_ollama_model=='':
                st.error("Please select an Ollama model")

            llm=ChatOllama(model=selected_ollama_model)

        except Exception as e:
            raise ValueError(f"Error Ocuured With Exception : {e}")
        return llm

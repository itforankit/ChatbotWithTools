import streamlit as st
import os
from datetime import date

from langchain_core.messages import AIMessage,HumanMessage
from uiconfigfile import Config
from pdfassistant import get_pdf_text, get_text_chunks, get_vector_store, get_conversational_chain

class LoadStreamlitUI:
    def __init__(self):
        self.config =  Config() # config
        self.user_controls = {}

    def initialize_session(self):
        return {
        "current_step": "requirements",
        "requirements": "",
        "user_stories": "",
        "po_feedback": "",
        "generated_code": "",
        "review_feedback": "",
        "decision": None
    }
  


    def load_streamlit_ui(self):
        st.set_page_config(page_title= " " + self.config.get_page_title(), layout="wide")
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(r".\Coforge.jpg")
        with col2:
           #st.markdown("<h1 style='text-align: left;'>",self.config.get_page_title(),"</h1>", unsafe_allow_html=True)
           st.header(self.config.get_page_title())
       # st.image(r".\src\langgraphagenticai\ui\Coforge.jpg") + "" + st.header(self.config.get_page_title())
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False
        st.session_state.IsSDLC = False
        
        

        with st.sidebar:
            # Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            provider=st.radio("Select Provider:", llm_options)
           # print(provider)
            self.user_controls["Provider"] = provider
           # print(self.user_controls["Provider"])

            if provider == "Groq":
                model_options = self.config.get_groq_model_options()
                selected_model = st.selectbox("Select Groq Model:", model_options)
            elif provider == "OpenAI":
                model_options = self.config.get_OpenAI_model_options()
                selected_model = st.selectbox("Select OpenAI Model:", model_options)

            self.user_controls["Models"] = selected_model
            # Use case selection
            self.user_controls["selected_usecase"] = st.selectbox("Select Usecases", usecase_options)
            
            allow_web_search=st.checkbox("Allow Web Search")
            self.user_controls["allow_web_search"]=allow_web_search
            
            st.write("📁 PDF File's Section")
            pdf_docs = st.file_uploader("Upload your PDF Files & \n Click on the Submit & Process Button ", accept_multiple_files=True)
            if st.button("Submit & Process"):
                    with st.spinner("Processing..."): # user friendly message.
                        raw_text = get_pdf_text(pdf_docs) # get the pdf text
                        text_chunks = get_text_chunks(raw_text) # get the text chunks
                        get_vector_store(text_chunks) # create vector store
                        st.success("Done")
            
            if "state" not in st.session_state:
                st.session_state.state = self.initialize_session()
            
            #self.render_requirements()
        
        return self.user_controls
    


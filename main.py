import streamlit as st
import json
from loadui import LoadStreamlitUI
#from src.langgraphagenticai.LLMs.groqllm import GroqLLM
#from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from display_result import DisplayResultStreamlit


# MAIN Function START
def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while 
    implementing exception handling for robustness.
    """
   
    # Load UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

   
    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return

    # Text input for user message
    if st.session_state.IsFetchButtonClicked:
        print("Hello")
        user_message = st.session_state.timeframe 
    else :
        print("Hello1")
        user_message = st.chat_input("Enter your message:")

    if user_message:
            #try:
                usecase = user_input.get('selected_usecase')
                if not usecase:
                    st.error("Error: No use case selected.")
                    return
                
                provider=user_input['Provider']
                if not provider:
                    st.error("Error: Please select Model provider.")
                    return
                
                selected_model=user_input['Models']
                if not selected_model:
                    st.error("Error: Please select Model.")
                    return
                
                allow_web_search=user_input["allow_web_search"]

                API_URL="http://127.0.0.1:9999/chat"

                if user_message.strip():
                    #Connect with backend vai url
                    import requests

                    payload={
                        "model_name": selected_model,
                        "model_provider": provider,
                        "system_prompt": "Agent",
                        "messages": [user_message],
                        "allow_search": allow_web_search
                            }

                    response=requests.post(API_URL, json=payload)
                    if response.status_code == 200:
                        response_data = response.json()
                        if "error" in response_data:
                            st.error(response_data["error"])
                        else:
                            st.subheader("Agent Response")
                            st.markdown(f"**Final Response:** {response_data}")

                ### Graph Builder
                
                #try:
                #    DisplayResultStreamlit(usecase,user_message).display_result_on_ui()
                #except Exception as e:
                #    st.error(f"Error: Graph setup failed - {e}")
                #    #st.write("Tools Available:", combinedtools)
                #    return
                

            #except Exception as e:
            #     raise ValueError(f"Error Occurred with Exception : {e}")
            

        

   

    

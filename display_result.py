import streamlit as st
#from langchain_core.messages import HumanMessage,AIMessage
import json
from IPython.display import Image, display
from PIL import Image
import io
from langchain.schema import HumanMessage


class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase= usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase= self.usecase
        graph = self.graph
        user_message = self.user_message

        if usecase =="Basic Chatbot":
                for event in graph.stream({'messages':("user",user_message)}):
                    print(event.values())
                    for value in event.values():
                        print(value['messages'])
                        with st.chat_message("user"):
                            st.write(user_message)
                        with st.chat_message("assistant"):
                            st.write(value["messages"].content)
        elif usecase=="Chatbot with Tools":
            for event in graph.stream({'messages':("user",user_message)}):
                    print(event.values())
                    for value in event.values():
                        print(value['messages'])
                        with st.chat_message("user"):
                            st.write(user_message)
                        with st.chat_message("assistant"):
                            st.write(value["messages"].content)
       
       # Code written by me
        """
        if usecase =="Basic Chatbot":
                print("Basic Chatbot User Message", self.user_message)
                
                #graph_png = graph.get_graph().draw_mermaid_png()
                #image = Image.open(io.BytesIO(graph_png))
                #desired_width = 200
                #desired_height = 200
                #graph_image=image.resize((desired_width, desired_height))
                # Display the image in the Streamlit app
                #st.image(graph_image, caption="Graph Visualization", use_column_width=True) 
                # Use a list of message dictionaries for the state.
                initial_state = {"messages": [HumanMessage(content=user_message)]}

                # Display the user message once.
                with st.chat_message("user"):
                  st.write(user_message)
                
                for event in graph.stream(initial_state):
                    #print("event ",event)
                    #for value in event.values():
                    #    print(user_message)
                    #    with st.chat_message("user"):
                    #        st.write(user_message)
                    #    with st.chat_message("assistant"):
                    #        st.write(value["messages"].content)
                     # Check if the event has an LLM response.
                    if "llm_response" in event:
                        assistant_response = event["llm_response"]
                        with st.chat_message("assistant"):
                            st.write(assistant_response)
            
                    # Alternatively, if the event includes a list of messages, iterate over them.
                    elif "messages" in event:
                        for msg in event["messages"]:
                             if hasattr(msg, "content"):
                                with st.chat_message("assistant"):
                                    st.write(msg.content)
        """
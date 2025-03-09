#step1 Setup API Keys
import os
from dotenv import load_dotenv
load_dotenv()
from langchain.tools import Tool
from PDFAssistant import PDFAssistant
from langchain.agents import initialize_agent
#from langchain.tools import Tool
from langgraph.graph import StateGraph

 

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY=os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_PROJECT=os.getenv("LANGCHAIN_PROJECT")
TAVILANG_API_KEY=os.getenv("TAVILY_API_KEY")
##
#os.environ["LANGGRAPH_RECURSION_LIMIT"] = "50"
#graph.invoke({...}, {"recursion_limit": 100})


# Step2 : Setip LLM & tools
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

openai_llm=ChatOpenAI(model="gpt-4o-mini")
groq_llm=ChatGroq(model="llama-3.3-70b-versatile",)

#Step3: Setup AI Agent with search tool functionality

#Agent
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
system_prompt="I am an AI assistant that can help you with your queries. I can provide you with information, answer your questions, and help you with your search queries. How can I help you today?"

#def add_tool(agent, new_tool):
#    agent.tools.append(new_tool)

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider,pdf_assistant):
    if provider=="Groq":
        llm=ChatGroq(model=llm_id)
    elif provider=="OpenAI":
        llm=ChatOpenAI(model=llm_id)

    tools=[TavilySearchResults(max_results=2)] if allow_search else []
    
    print(tools)
    #config = {"recursion_limit": 50}  # Increase the recursion limit
    #agent = create_react_agent(llm, tools, config=config)
    agent=create_react_agent(
        model=groq_llm,
        tools=tools,
        state_modifier=system_prompt
        #config=config
        )
  

    print("PDF Assistant status: ",pdf_assistant)
    #pdf_assistant=True
    if pdf_assistant:
        #pdf_path = "sample.pdf"  # Replace with the actual PDF file path
        #openai_api_key = "your-api-key-here"  # Replace with your OpenAI API key
        PDFAssist = PDFAssistant(OPENAI_API_KEY)

        # Define a tool to integrate with the agent
        def pdf_search_tool(query):
            """Calls PDFAssistant's search function."""
            results = PDFAssist.search(query)
            print("pdf asstsant : " ,results)
            return "\n".join(results)

        #pdf_tool = Tool(
        #    name="PDF Search",
        #    func=pdf_search_tool,
        #    description="Use this tool to search for information within the provided PDF."
        #)

        def define_tools():
            print("pdf search")
            return Tool(
            name="PDF Search",
            func=pdf_search_tool,
            description="Use this tool to search for information within the provided PDF."
            )
        pdf_tool = define_tools()  # ✅ Now pdf_tool is accessible  
        print(type(agent))
        print(dir(agent))
        #agent.tools.append(pdf_tool)
        #print("After adding PDF Assistant tool ",tools)
        # ✅ Pass multiple tools in a list
        #tools = [pdf_tool, tools]

        # ✅ Create the agent with multiple tools
        agent = create_react_agent(groq_llm, [pdf_tool])
        #agent = create_react_agent(groq_llm, tools=[pdf_tool,tools])
        #graph = agent.compile(recursion_limit=50)
        #graph.config(recursion_limit=50) 
        

    #query="Tell me about the trends in crypto markets"
    print("After adding PDF Assistant tool ",tools)
    state={"messages":query}
    response=agent.invoke(state)
    message=response.get("messages")
    #response=agent.stream(state)
    # for step in agent.stream({"input": state}):
    #     response = step  # Keep updating with the latest response
    #     print(step)

    # # ✅ Now extract the "messages" safely
    # if response and isinstance(response, dict):  
    #     message = response.get("messages")
    #     print(message)
    # else:
    #     print("No valid response received.")

    ai_message=[message.content for message in message if isinstance(message,AIMessage)]    

    return ai_message[-1]






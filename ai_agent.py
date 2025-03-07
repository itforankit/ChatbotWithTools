#step1 Setup API Keys
import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY=os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_PROJECT=os.getenv("LANGCHAIN_PROJECT")
TAVILANG_API_KEY=os.getenv("TAVILY_API_KEY")


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

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    if provider=="Groq":
        llm=ChatGroq(model=llm_id)
    elif provider=="OpenAI":
        llm=ChatOpenAI(model=llm_id)

    tools=[TavilySearchResults(max_results=2)] if allow_search else []

    agent=create_react_agent(
        model=groq_llm,
        tools=tools,
        state_modifier=system_prompt
    )

    #query="Tell me about the trends in crypto markets"

    state={"messages":query}
    response=agent.invoke(state)
    message=response.get("messages")
    ai_message=[message.content for message in message if isinstance(message,AIMessage)]    

    return ai_message[-1]






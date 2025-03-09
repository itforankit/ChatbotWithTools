from langchain.agents import initialize_agent
from langchain.tools import Tool
from langchain.chat_models import ChatOpenAI

# Initialize PDFAssistant
pdf_path = "sample.pdf"  # Replace with your actual PDF path
openai_api_key = "your-api-key-here"  # Replace with your OpenAI API key

pdf_assistant = PDFAssistant(pdf_path, openai_api_key)

# Define a tool to integrate with the agent
def pdf_search_tool(query):
    """Calls PDFAssistant's search function."""
    results = pdf_assistant.search(query)
    return "\n".join(results)

pdf_tool = Tool(
    name="PDF Search",
    func=pdf_search_tool,
    description="Use this tool to search for information within the provided PDF."
)

# Define the list of tools
tools = [pdf_tool]

# Initialize the React-based agent
groq_llm = ChatOpenAI(model_name="gpt-4")  # Change to your preferred model

agent = initialize_agent(
    tools=tools,
    llm=groq_llm,
    agent="react",  # ReAct-style agent
    verbose=True  # Set to False in production
)

# Example interaction
query = "What is the main topic of the document?"
response = agent.run(query)

print("\nAgent Response:")
print(response)

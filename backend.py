#setup pydantic model
from pydantic import BaseModel
from typing import List

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool





#setup AI agent from frontend request
from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent

app = FastAPI(title="AI Agent")

ALLOWED_MODEL_NAMES=["llama-3.3-70b-versatile","gpt-4o-mini","mixtral-8x7b-32768"]

@app.post("/chat")
def chat_endpoint(request: RequestState):
   """
   API Endpoint to interact with the chatbot using langraph and search tools.
   It dynamically selects the model specified in the request.
   """
   if request.model_name not in ALLOWED_MODEL_NAMES:
       return {"error":"Invalid model name"}
   
   #Create AI Agent and get response from it
   response=get_response_from_ai_agent(
       llm_id=request.model_name,
       query=request.messages,
       allow_search=request.allow_search,
       system_prompt=request.system_prompt,
       provider=request.model_provider
   )
   return response

# run app & explore swagger UI docs
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1",port=9999)

    # run uusing python backend.py
    # open the url
    # use doc for postman test
"""
    {
  "model_name": "llama-3.3-70b-versatile",
  "model_provider": "Groq",
  "system_prompt": "Act as a helpul AI",
  "messages": [
    "What is the capital of Australia"
  ],
  "allow_search": false
}
"""
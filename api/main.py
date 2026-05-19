from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str

@app.get("/api/main")
def read_root():
    return {"message": "Python Backend for Agent Router on Vercel is Live 24/7!"}

@app.post("/api/chat")
def chat_with_ai(request: ChatRequest):
    agent_router_url = "https://agentrouter.org/v1/chat/completions"
    api_key = "Sk-7eeoGOHiiviyMTB6Rxe87lOnB7rGgto8FR8JKmDztKpmriZX"

    payload = {
        "model": "claude-3-5-sonnet",
        "messages": [{"role": "user", "content": request.prompt}],
        "stream": False
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(agent_router_url, json=payload, headers=headers, timeout=25)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Agent Router Error: {response.text}")
            
        return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


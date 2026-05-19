from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from curl_cffi import requests

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

@app.get("/")
def read_root():
    return {"message": "All-Time Live Agent Router Backend with TLS Spoofing!"}

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
        "Content-Type": "application/json",
    }

    try:
        # impersonate="chrome" lagane se yeh exact Google Chrome browser ki tarah TLS request generate karega
        # Isse Cloudflare ka firewall data center ke IP par bhi check pass kar deta hai
        response = requests.post(
            agent_router_url, 
            json=payload, 
            headers=headers, 
            impersonate="chrome", 
            timeout=30
        )
        
        # Safe response parsing
        return response.json()

    except Exception as e:
        # Agar koi format issue ho ya error aaye
        raise HTTPException(status_code=500, detail=f"Bypass Error: {str(e)}")

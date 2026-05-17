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

@app.get("/")
def read_root():
    return {"message": "Python Backend Firewall Bypass Active!"}

@app.post("/api/chat")
def chat_with_ai(request: ChatRequest):
    # Agent Router ka default completion endpoint
    agent_router_url = "https://agentrouter.org/v1/chat/completions"
    api_key = "Sk-7eeoGOHiiviyMTB6Rxe87lOnB7rGgto8FR8JKmDztKpmriZX"

    payload = {
        "model": "claude-3-5-sonnet",
        "messages": [
            {"role": "user", "content": request.prompt}
        ],
        "stream": False
    }

    # CRITICAL: Real browser ke headers add kiye hain taaki Cloudflare block na kare
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.5 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "Origin": "https://agentrouter.org",
        "Referer": "https://agentrouter.org/"
    }

    try:
        response = requests.post(agent_router_url, json=payload, headers=headers)
        
        # Agar abhi bhi HTML page bhejta hai, toh handle karein
        if "application/json" not in response.headers.get("Content-Type", ""):
            return {
                "choices": [{
                    "message": {
                        "content": f"⚠️ Cloudflare Security Blocked (Status {response.status_code}). Base URL badalna padega."
                    }
                }]
            }

        return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

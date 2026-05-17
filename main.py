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
    return {"message": "Python Backend is ready!"}

@app.post("/api/chat")
def chat_with_ai(request: ChatRequest):
    # Anthropic Messages format endpoint use kar rahe hain
    agent_router_url = "https://agentrouter.org/v1/messages"
    api_key = "Sk-7eeoGOHiiviyMTB6Rxe87lOnB7rGgto8FR8JKmDztKpmriZX"

    # Anthropic standard payload structure
    payload = {
        "model": "claude-3-5-sonnet",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": request.prompt}
        ]
    }

    headers = {
        "x-api-key": api_key,          # Anthropic API Key header
        "anthropic-version": "2023-06-01", # Required for Anthropic style proxies
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(agent_router_url, json=payload, headers=headers)
        
        # Agar fir bhi HTML mile, toh error details return karein taaki debug ho sake
        if "application/json" not in response.headers.get("Content-Type", ""):
            raise HTTPException(
                status_code=502, 
                detail=f"Status {response.status_code}. Agent Router HTML return kar raha hai."
            )

        return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

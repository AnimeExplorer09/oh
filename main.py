from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# Render par CORS block na ho, isliye setup
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
    return {"message": "Python FastAPI Backend is Live!"}

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
        "Accept": "application/json"
    }

    try:
        response = requests.post(agent_router_url, json=payload, headers=headers)
        
        # HTML template error ko block karne ke liye check
        if "application/json" not in response.headers.get("Content-Type", ""):
            raise HTTPException(
                status_code=502, 
                detail="Agent Router returned an invalid HTML page instead of JSON."
            )

        return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    return {"message": "Python Backend Spy Mode Active!"}

@app.post("/api/chat")
def chat_with_ai(request: ChatRequest):
    # Base URL ko test karne ke liye
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
        
        # AGAR HTML AAYA: Toh crash mat karo, balki us HTML ka text content nikal kar return karo!
        if "application/json" not in response.headers.get("Content-Type", ""):
            raw_html = response.text
            # Agar unhone response me kuch text likha hai, toh use extract karo
            import re
            clean_text = re.sub('<[^<]+?>', '', raw_html).strip() # Saari HTML tags gayab
            clean_text = " ".join(clean_text.split())[:300] # Pehle 300 words check karne ke liye
            
            return {
                "choices": [{
                    "message": {
                        "content": f"⚠️ Server returned HTML text: {clean_text}"
                    }
                }]
            }

        return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

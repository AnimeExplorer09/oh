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
    return {"message": "Agent Router Termux-Style Backend is Live!"}

@app.post("/api/chat")
def chat_with_ai(request: ChatRequest):
    agent_router_url = "https://agentrouter.org/v1/chat/completions"
    api_key = "Sk-7eeoGOHiiviyMTB6Rxe87lOnB7rGgto8FR8JKmDztKpmriZX"

    payload = {
        "model": "claude-3-5-sonnet",
        "messages": [{"role": "user", "content": request.prompt}],
        "stream": False
    }

    # Termux aur Android browser ka exact fingerprint mimic karne ke liye headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Ch-Ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site"
    }

    try:
        # Ek fresh session banakar call karenge taaki cookie block na ho
        session = requests.Session()
        response = session.post(agent_router_url, json=payload, headers=headers, timeout=20)
        
        # Check agar fir bhi HTML de raha hai
        if "application/json" not in response.headers.get("Content-Type", ""):
            raise HTTPException(
                status_code=502, 
                detail="Cloudflare ne Render IP ko fir se catch kar liya. Aap ek baar frontend refresh karke bhejiyega."
            )

        return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

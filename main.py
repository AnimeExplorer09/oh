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
    return {"message": "24/7 Anti-Block Agent Router Backend is Live!"}

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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    # Free public proxy to mask Render's data-center IP
    # Yeh request ko ek normal internet user ki tarah bhejega
    proxies = {
        "http": "http://pubproxy.com/api/proxy",
        "https": "http://pubproxy.com/api/proxy"
    }

    try:
        # Pehle proxy ke sath try karenge, agar proxy slow ho toh bina proxy ke backup check lagaya hai
        try:
            response = requests.post(agent_router_url, json=payload, headers=headers, proxies=proxies, timeout=15)
        except Exception:
            # Backup: Ek aur free proxy alternative anoymous route
            alt_proxy = {"https": "http://185.193.157.43:8080"} 
            response = requests.post(agent_router_url, json=payload, headers=headers, proxies=alt_proxy, timeout=15)

        # Agar JSON response mil gaya, toh Cloudflare bypass ho gaya!
        if "application/json" in response.headers.get("Content-Type", ""):
            return response.json()
            
        # Fallback handling agar fir bhi HTML page pakda de
        raise HTTPException(
            status_code=502, 
            detail="Firewall block bypass temporary issue. Ek baar fir se send button dabayein."
        )

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

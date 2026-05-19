from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cloudscraper
import json

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
    return {"message": "All-Time Live Cloudscraper Agent Router Backend!"}

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
        # cloudscraper khud Cloudflare ke anti-bot browser challenge ko automatically execute aur solve karega
        scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
        
        response = scraper.post(agent_router_url, data=json.dumps(payload), headers=headers, timeout=30)
        
        # Pehle check karenge ki response proper mila ya nahi
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Server returned status {response.status_code}")
            
        try:
            return response.json()
        except Exception:
            raise HTTPException(status_code=502, detail="Cloudscraper ke baad bhi HTML page mila. Agent Router IP level par block kar raha hai.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraper Error: {str(e)}")

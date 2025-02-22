from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

@app.get("/")
async def root():
    return {
        "service": "LLM Service",
        "status": "running",
        "endpoints": [
            {"path": "/v1/chat/completions", "method": "POST", "description": "Create chat completions"}
        ]
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    model: str
    max_tokens: int = 100
    temperature: float = 0.7

@app.post("/v1/chat/completions")
async def create_completion(request: ChatRequest):
    try:
        return {
            "model": request.model,
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": "This is a test response"
                }
            }]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
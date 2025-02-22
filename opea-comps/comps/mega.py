from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import httpx

app = FastAPI()

@app.get("/")
async def root():
    return {
        "service": "Mega Service",
        "status": "running",
        "endpoints": [
            {"path": "/v1/example-service", "method": "POST", "description": "Process messages through embedding and LLM"}
        ]
    }

@app.get("/health")
async def health():
    try:
        async with httpx.AsyncClient() as client:
            embedding_health = await client.get("http://embedding:6000/health")
            llm_health = await client.get("http://llm:9000/health")
            return {
                "status": "healthy",
                "embedding": embedding_health.json(),
                "llm": llm_health.json()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    model: str
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7

@app.post("/v1/example-service")
async def example_service(request: ChatRequest):
    try:
        async with httpx.AsyncClient() as client:
            # Call embedding service
            embedding_response = await client.post(
                "http://embedding:6000/v1/embeddings",
                json={"model": "text-embedding-ada-002", "messages": request.messages[0].content}
            )
            
            # Call LLM service
            llm_response = await client.post(
                "http://llm:9000/v1/chat/completions",
                json=request.model_dump()
            )
            
            return {
                "embedding_result": embedding_response.json(),
                "llm_result": llm_response.json()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
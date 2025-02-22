from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Add root endpoint for browser
@app.get("/")
async def root():
    return {
        "service": "Embedding Service",
        "status": "running",
        "endpoints": [
            {"path": "/v1/embeddings", "method": "POST", "description": "Create embeddings"}
        ]
    }

# Add health check
@app.get("/health")
async def health():
    return {"status": "healthy"}

class EmbeddingRequest(BaseModel):
    model: str
    messages: str

@app.post("/v1/embeddings")
async def create_embedding(request: EmbeddingRequest):
    try:
        return {
            "model": request.model,
            "embedding": [0.1, 0.2, 0.3],  # Placeholder embedding
            "message": request.messages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
import os
import uvicorn
from fastapi import FastAPI
from comps import MicroService, ServiceOrchestrator, ServiceType

app = FastAPI()
service_type = os.getenv("SERVICE_TYPE")
port = int(os.getenv("SERVICE_PORT", "8000"))

if service_type == "embedding":
    service = MicroService(
        name="embedding",
        host="0.0.0.0",
        port=port,
        endpoint="/v1/embeddings",
        use_remote_service=True,
        service_type=ServiceType.EMBEDDING
    )
    # Add embedding routes
    @app.post("/v1/embeddings")
    async def create_embedding():
        return {"message": "Embedding service"}

elif service_type == "llm":
    service = MicroService(
        name="llm",
        host="0.0.0.0",
        port=port,
        endpoint="/v1/chat/completions",
        use_remote_service=True,
        service_type=ServiceType.LLM
    )
    # Add LLM routes
    @app.post("/v1/chat/completions")
    async def create_completion():
        return {"message": "LLM service"}

else:
    # Mega-service orchestrator
    orchestrator = ServiceOrchestrator()
    @app.get("/")
    async def root():
        return {"message": "Mega service orchestrator"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port) 
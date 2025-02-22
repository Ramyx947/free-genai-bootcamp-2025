import os
import uvicorn
from fastapi import FastAPI

# Import the appropriate app based on service type
service_type = os.getenv("SERVICE_TYPE", "mega")
port = int(os.getenv("SERVICE_PORT", "8000"))

if service_type == "embedding":
    from .embedding import app
elif service_type == "llm":
    from .llm import app
else:
    from .mega import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port) 
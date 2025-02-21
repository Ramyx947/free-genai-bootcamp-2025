from enum import Enum

class ServiceType(Enum):
    EMBEDDING = "embedding"
    LLM = "llm"

class MicroService:
    def __init__(self, name, host, port, endpoint, use_remote_service, service_type):
        self.name = name
        self.host = host
        self.port = port
        self.endpoint = endpoint
        self.use_remote_service = use_remote_service
        self.service_type = service_type

class ServiceOrchestrator:
    def __init__(self):
        self.services = []

    def add(self, service):
        self.services.append(service)
        return self

    def flow_to(self, service1, service2):
        # Add flow logic here
        pass 
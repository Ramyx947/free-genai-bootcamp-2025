from comps import MicroService, ServiceOrchestrator, ServiceType

def test_service_creation():
    # Create orchestrator
    orchestrator = ServiceOrchestrator()
    
    # Create services
    embedding = MicroService(
        name="embedding",
        host="0.0.0.0",
        port=6000,
        endpoint="/v1/embeddings",
        use_remote_service=True,
        service_type=ServiceType.EMBEDDING
    )
    
    llm = MicroService(
        name="llm",
        host="0.0.0.0",
        port=9000,
        endpoint="/v1/chat/completions",
        use_remote_service=True,
        service_type=ServiceType.LLM
    )
    
    # Add services
    orchestrator.add(embedding).add(llm)
    orchestrator.flow_to(embedding, llm)
    
    # Verify services are added
    assert len(orchestrator.services) == 2
    print("Test passed: Services created and added successfully!")

if __name__ == "__main__":
    test_service_creation() 
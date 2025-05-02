import requests

def test_question_generation():
    # Test data
    test_text = "Bună ziua! Vremea este frumoasă astăzi în România."
    
    # Make request to local service
    try:
        response = requests.post(
            "http://localhost:8002/generate-questions",
            json={"text": test_text, "num_questions": 1}
        )
        
        print("\nRequest sent successfully!")
        print("\nResponse status:", response.status_code)
        print("\nResponse data:", response.json())
        
    except Exception as e:
        print(f"Error testing service: {str(e)}")

if __name__ == "__main__":
    test_question_generation() 
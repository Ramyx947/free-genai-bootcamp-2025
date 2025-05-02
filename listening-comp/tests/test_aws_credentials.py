import boto3
import json
from dotenv import load_dotenv
import os

def test_polly_access():
    # Load environment variables
    load_dotenv()
    
    # Debug: Print credentials status (not the actual values)
    print("Checking AWS credentials...")
    print(f"Access Key ID present: {'Yes' if os.getenv('AWS_ACCESS_KEY_ID') else 'No'}")
    print(f"Secret Key present: {'Yes' if os.getenv('AWS_SECRET_ACCESS_KEY') else 'No'}")
    print(f"Region: {os.getenv('AWS_DEFAULT_REGION', 'Not set')}")
    
    try:
        # Initialize Polly client
        polly = boto3.client('polly')
        
        # Test a simple request
        response = polly.describe_voices(
            LanguageCode='ro-RO'
        )
        
        print("\nSuccessfully connected to Polly!")
        print("\nAvailable Romanian voices:")
        for voice in response['Voices']:
            print(f"- {voice['Name']} ({voice['Gender']})")
            
    except Exception as e:
        print(f"\nError connecting to Polly: {str(e)}")
        print("Please check your AWS credentials and permissions.")

if __name__ == "__main__":
    test_polly_access() 
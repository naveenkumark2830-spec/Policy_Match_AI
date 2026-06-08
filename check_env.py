import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(verbose=True)

# Check if key exists
api_key = os.getenv("GROQ_API_KEY")

if api_key:
    print("SUCCESS: GROQ_API_KEY found")
    print(f"Key starts with: {api_key[:10]}...")
else:
    print("ERROR: GROQ_API_KEY not found")
    print("Check your .env file")
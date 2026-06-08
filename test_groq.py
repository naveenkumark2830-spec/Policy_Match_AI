import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print(f"API Key loaded: {api_key is not None}")

try:
    client = Groq(api_key=api_key)
    print("SUCCESS: Groq client initialized")
    
    # Test API call
    msg = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Say OK"}],
        max_tokens=10
    )
    
    print(f"API Response: {msg.choices[0].message.content}")
    
except Exception as e:
    print(f"ERROR: {e}")
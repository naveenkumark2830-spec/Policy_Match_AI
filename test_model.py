import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

models = [
    "llama-3.3-70b-versatile",
    "llama-3.1-405b-reasoning", 
    "gemma-2-9b-it"
]

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

for model in models:
    try:
        print(f"Testing {model}...", end=" ")
        msg = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )
        print("SUCCESS")
    except Exception as e:
        error_msg = str(e)
        if "decommissioned" in error_msg:
            print("DEPRECATED")
        else:
            print(f"ERROR: {error_msg[:50]}")
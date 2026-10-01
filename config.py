import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Get Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Get model name
MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")

# Check if API key exists
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in .env")

print("Configuration loaded successfully!")
print("Model:", MODEL)
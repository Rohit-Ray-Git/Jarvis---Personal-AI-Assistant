# llm.py
# Placeholder for LLM integration commands (OpenAI, local models, etc.) 

import os
import requests
from dotenv import load_dotenv
from config import ASSISTANT_NAME

# Load environment variables from .env
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1/chat/completions")

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://your-site-or-project.com",
    "X-Title": "Jarvis Assistant"
}

def get_llm_response(user_text):
    if not OPENROUTER_API_KEY:
        return f"[OpenRouter API key not set] You said: {user_text}"
    data = {
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [
            {"role": "system", "content": f"You are {ASSISTANT_NAME}, a helpful AI assistant."},
            {"role": "user", "content": user_text}
        ]
    }
    try:
        response = requests.post(OPENROUTER_API_URL, headers=HEADERS, json=data)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            return f"[OpenRouter API error {response.status_code}] {response.text}"
    except Exception as e:
        return f"[Error contacting OpenRouter: {e}]" 
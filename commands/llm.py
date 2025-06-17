# llm.py
# Placeholder for LLM integration commands (OpenAI, local models, etc.) 

import os
import requests
from dotenv import load_dotenv
from config import ASSISTANT_NAME

# Load environment variables from .env
load_dotenv()

# Azure OpenAI config
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# OpenRouter fallback
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1/chat/completions")

HEADERS_OPENROUTER = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://your-site-or-project.com",
    "X-Title": "Jarvis Assistant"
}

def get_llm_response(user_text):
    # Prefer Azure OpenAI if configured
    if AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY and AZURE_OPENAI_DEPLOYMENT:
        url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2023-03-15-preview"
        headers = {
            "api-key": AZURE_OPENAI_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "messages": [
                {"role": "system", "content": f"You are {ASSISTANT_NAME}, a helpful AI assistant."},
                {"role": "user", "content": user_text}
            ]
        }
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[Azure OpenAI error: {e}]"
    # Fallback to OpenRouter
    elif OPENROUTER_API_KEY:
        data = {
            "model": "openai/gpt-4o-2024-11-20",
            "messages": [
                {"role": "system", "content": f"You are {ASSISTANT_NAME}, a helpful AI assistant."},
                {"role": "user", "content": user_text}
            ]
        }
        try:
            response = requests.post(OPENROUTER_API_URL, headers=HEADERS_OPENROUTER, json=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                return f"[OpenRouter API error {response.status_code}] {response.text}"
        except Exception as e:
            return f"[Error contacting OpenRouter: {e}]"
    else:
        return f"[No LLM API configured] You said: {user_text}" 
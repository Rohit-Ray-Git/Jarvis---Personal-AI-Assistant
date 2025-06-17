import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

prompt = "What is the capital of France?"

if AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY and AZURE_OPENAI_DEPLOYMENT:
    url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2023-03-15-preview"
    headers = {
        "api-key": AZURE_OPENAI_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "messages": [
            {"role": "system", "content": "You are Jarvis, a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        resp_json = response.json()
        print("Full Azure OpenAI response:")
        print(json.dumps(resp_json, indent=2))
        if "choices" in resp_json and resp_json["choices"]:
            print("\nModel used:", resp_json.get("model", "(not specified)"))
            print("\nAzure OpenAI answer:")
            print(resp_json["choices"][0]["message"]["content"])
        else:
            print("No choices in response.")
    except Exception as e:
        print(f"[Azure OpenAI error: {e}]")
else:
    print("Azure OpenAI environment variables not set.") 
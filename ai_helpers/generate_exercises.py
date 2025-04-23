import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # set this in your environment or .env file
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama3-8b-8192"

def generate_prompt(topic, difficulty="beginner"):
    return f"Create a {difficulty} Python exercise about {topic}, and provide a clear explanation for the answer."

def get_ai_response(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

def generate_exercise(topic):
    prompt = generate_prompt(topic)
    return get_ai_response(prompt)

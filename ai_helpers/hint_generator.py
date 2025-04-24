import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.3-70b-versatile"

def generate_hint(user_code, solution_code):
    prompt = f"""
    The user submitted this Python code:
    {user_code}

    The correct solution is:
    {solution_code}

    Please analyze the user code. If it's incorrect:
    - Explain what the user did wrong.
    - Provide a small hint (do NOT reveal the full solution).
    - If possible, include a short correction suggestion (not full code).

    Return only helpful guidance, like a Python tutor would.
    """

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "⚠️ Sorry, couldn't generate a hint right now."

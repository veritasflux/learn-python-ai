import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.3-70b-versatile"

def generate_hint(user_code, solution_code):
    prompt = f"""
            You are an expert Python tutor helping students learn by doing.
            
            The student submitted this code:
            \"\"\"
            {user_code}
            \"\"\"
            
            The expected solution is:
            \"\"\"
            {solution_code}
            \"\"\"
            
            Your job:
            1. Determine whether the student's code is logically and syntactically correct.
            2. If it's correct but structured differently (e.g., different variable names or formatting), you should still consider it correct. Provide a compliment and optionally suggest minor improvements (e.g., naming clarity).
            3. If it's incorrect, do NOT reveal the correct solution. Instead:
               - Gently point out what seems to be wrong.
               - Suggest what the student might reconsider.
               - Give one small tip or question to guide them toward the correct approach.
            4. Never reveal the full correct solution.
            5. Do not require exact output values unless absolutely necessary — focus on logic.
            6. Accept all different variable names, constants, and formatting styles as long as the logic is valid.
            7. Output your answer strictly as a JSON object with this format:
            
            {{
              "is_correct": true or false,
              "feedback": "your explanation or hint here"
            }}
            
            Do not add any commentary or explanation outside the JSON response.
            """

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "response_format": {"type": "json_object"},
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "⚠️ Sorry, couldn't generate a hint right now."

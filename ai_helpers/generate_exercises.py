import os
import requests
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # set this in your environment or .env file
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama3-8b-8192"

def generate_prompt(topic, difficulty="beginner"):
    # Modify the prompt to instruct the model to return the exercise in JSON format
    return rf"""
    Create a {difficulty} Python exercise about {topic}. 
    Make the question dynamic and fresh each time:
    - Randomize variable values or names
    - Use small real-world contexts
    - Avoid exercises with imports and input function
    - Always give detailed specifications (number, price, quantity, size ...)
    Your response MUST be a single, valid JSON object starting with {{ and ending with }}. Do not include any text before or after the JSON object.
    Adhere strictly to the following JSON structure:
    
    {{
      "question": "A clear and concise question prompt asking the user to write the Python code.",
      "solution": {{
        "code": "The complete Python code solution provided as a single JSON string. Ensure all special characters within this code string, such as quotes (\\") and newlines (\\n), are correctly escaped.",
        "explanation": "A step-by-step explanation of the Python code solution, also as a JSON string with proper escaping."
      }}
    }}
    
    Ensure that the output is valid JSON and can be parsed using json.loads().
    """


def get_ai_response(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "response_format": {"type": "json_object"},
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=body)
    if response.status_code == 200:
        try:
            # Attempt to parse the response as JSON
            ai_response = response.json()["choices"][0]["message"]["content"]
            print(ai_response)
            return json.loads(ai_response)  # Parse the string into a JSON object
        except json.JSONDecodeError:
            return f"Error: Response is not in valid JSON format."
    else:
        return f"Error: {response.status_code} - {response.text}"

def generate_exercise(topic):
    prompt = generate_prompt(topic)
    return get_ai_response(prompt)

# ai_helpers/generate_slide_explanation.py
import os
import requests
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # set this in your environment or .env file
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama3-70b-8192"

def generate_batch_explanation(slides):
    """
    Generates explanations for a batch of slides in a single API call.
    The input is a list of slide contents, and the output is a JSON object with
    slide titles as keys and their corresponding explanations as values.
    """
    # Prepare a prompt that includes all slides for explanation generation
    slide_contents = "\n\n".join([f"Slide {index+1}: {slide['content']}" for index, slide in enumerate(slides)])
    
    prompt = f"""
    You are an expert Python teacher. For each slide, provide a detailed, beginner-friendly explanation of the content. Make it fun.
    The slides are:
    
    {slide_contents}
    
    For each slide, return a detailed explanation in simple terms, possibly with examples, to help beginners understand the concept. Respond in JSON format where each slide number is mapped to its corresponding explanation.
    
    Example output:
    {{
        "Slide 1": "Explanation for slide 1",
        "Slide 2": "Explanation for slide 2",
        ...
    }}
    """

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
            # Parse the response as JSON
            ai_response = response.json()["choices"][0]["message"]["content"]
            print(ai_response)
            return json.loads(ai_response)  # Parse into a JSON object
        except json.JSONDecodeError:
            return f"Error: Response is not in valid JSON format."
    else:
        return f"Error: {response.status_code} - {response.text}"

def fetch_slide_explanations(slides):
    """
    Fetches explanations for all slides and returns them as a JSON object.
    """
    return generate_batch_explanation(slides)

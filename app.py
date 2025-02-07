import streamlit as st
from openai import OpenAI
import os
import sys
import io

# Set Huggingface API key
client = OpenAI(
    base_url="https://huggingface.co/api/inference-proxy/together",
    api_key=os.getenv("HUGGING_API_KEY")
)

def get_ai_suggestion(user_input):
    prompt = f"""You are a helpful AI tutor for Python beginners.
    The user is learning Python and provided the following incomplete or incorrect code:
    
    ```python
    {user_input}
    ```

    Please complete or correct this code in a simple way, and explain briefly why.
    """
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1", 
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    
    # Extracting only the relevant response and ensuring it fits within the UI
    suggestion = response.choices[0].message.content
    suggestion = suggestion.split("</think>")[-1].strip()  # Remove <think> section if present
    return suggestion

def generate_lesson():
    prompt = "Create an interactive Python lesson for beginners, including explanations and coding examples."
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1", 
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.choices[0].message.content

def generate_exercise():
    prompt = "Based on the following lesson, create a simple exercise for beginners to practice Python:\n\n" + generate_lesson()
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1", 
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content

def execute_code(code):
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(code, {})
        output = sys.stdout.getvalue()
    except Exception as e:
        output = str(e)
    sys.stdout = old_stdout
    return output

# Streamlit UI
st.title("Python AI Learning - Lesson 1")
st.subheader("Introduction to Python")

# Generate AI-driven lesson
st.markdown("## Lesson Content")
st.markdown(generate_lesson())

# AI-Generated Exercise
st.markdown("## Try This Exercise")
st.markdown(generate_exercise())

# User Experiment: Interactive Coding Playground
st.markdown("## Your Coding Playground")
user_code = st.text_area("Write your Python code here:", "")

if st.button("Run Code"):
    output = execute_code(user_code)
    st.markdown("### Output:")
    st.code(output, language='text')

if st.button("Ask AI for Help"):
    suggestion = get_ai_suggestion(user_code)
    st.markdown("### AI Suggestion:")
    st.code(suggestion, language='python')

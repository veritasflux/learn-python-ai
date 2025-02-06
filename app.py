import streamlit as st
from openai import OpenAI
import os

# Set Huggingface API key
client = OpenAI(
    base_url="https://huggingface.co/api/inference-proxy/together",
    api_key=os.getenv("HUGGING_API_KEY")
)

def get_ai_suggestion(user_input):
    prompt = f"""You are a helpful AI tutor for Python beginners.
    The user is learning Python and provided the following code, which may be correct, incomplete or incorrect:
    
    ```python
    {user_input}
    ```
    If code correct, give back the code with congratulation and explanation of the function use.
    If code incorrect, please complete or correct this code in a simple way, and explain briefly why.
    Always use "```python" for code output.
    """
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1", 
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    
    # Extracting only the relevant response and ensuring it fits within the UI
    suggestion = response.choices[0].message.content
    suggestion = suggestion.split("</think>")[-1].strip()  # Remove <think> section if present
    
    # Split code and explanation
    lines = suggestion.split("```python")
    if len(lines) > 1:
        code_part = lines[1].split("```", 1)[0].strip()
        explanation_part = lines[-1].strip()
    else:
        code_part = suggestion.strip()
        explanation_part = ""
    
    return code_part, explanation_part

# Streamlit UI
st.title("Python AI Learning - Lesson 1")
st.subheader("Introduction to Python")

# Section 1: Welcome Message
st.write("Welcome to your first Python lesson! Python is a powerful and beginner-friendly programming language used in web development, data science, AI, and more.")

# Section 2: First Python Program
st.write("### Your First Python Program")
st.write("To display text in Python, we use the `print()` function. Try running this:")
st.code('print("Hello, world!")', language='python')

# User Experiment: Writing Print Statements
st.write("Now, try writing your own print statement below!")
user_code = st.text_area("Write Python code:", "print(")

if st.button("Get AI Suggestion"):
    code_suggestion, explanation = get_ai_suggestion(user_code)
    st.write("### AI Suggestion:")
    st.code(code_suggestion, language='python')
    if explanation:
        st.write("### Explanation:")
        st.write(explanation)

# Section 3: Quiz
st.write("### Quick Quiz")
st.write("Which of the following prints 'Hello, world!' correctly?")
quiz_options = ["print(Hello, world!)", "print(\"Hello, world!\")", "echo 'Hello, world!'"]
correct_answer = "print(\"Hello, world!\")"
user_answer = st.radio("Select the correct option:", quiz_options)

if st.button("Submit Answer"):
    if user_answer == correct_answer:
        st.success("✅ Correct! Great job!")
    else:
        st.error("❌ Not quite! Remember, Python requires quotes around strings.")

st.write("### AI-Powered Help")
st.write("💡 If you're stuck, the AI will suggest corrections!")

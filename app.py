import streamlit as st
from openai import OpenAI
import os
from groq import Groq

def get_ai_suggestion(user_input):
    client = Groq()
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
            {
                "role": "system",
                "content": f"""You are a helpful AI tutor for Python beginners.
                            The user is learning Python and provided the following incomplete or incorrect code:
                            
                            ```python
                            {user_input}
                            ```
                        
                            Please complete or correct this code in a simple way, and explain briefly why.
                            """
            },
            {
                "role": "user",
                "content": {user_input}
            }
        ],
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        stream=True,
        stop=None,
    )
    
    # Extracting only the relevant response and ensuring it fits within the UI
    suggestion = completion.choices[0].message.content
    suggestion = suggestion.split("</think>")[-1].strip()  # Remove <think> section if present
    return suggestion

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
    suggestion = get_ai_suggestion(user_code)
    st.write("### AI Suggestion:")
    st.markdown(suggestion, language='python')

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

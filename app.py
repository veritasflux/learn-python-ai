import streamlit as st
from openai import OpenAI
import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_TOKEN"))

def get_ai_suggestion(user_input):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""You are a helpful AI tutor for Python beginners.
                            The user is learning Python and provided the following code, which may be correct, incomplete or incorrect code:
                            If code correct, congratulate and explain briefly.
                            If code incorrect, please complete or correct this code in a simple way, and explain briefly why.
                            """
            },
            {
                "role": "user",
                "content":   f"""
                            ```python
                            {user_input}
                            ```
                            """
            }
        ],
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        stream=None,
        stop=None,
    )
    
    # Extracting only the relevant response and ensuring it fits within the UI
    suggestion = completion.choices[0].message.content
    suggestion = suggestion.split("</think>")[-1].strip()  # Remove <think> section if present
    return suggestion

def generate_exercise():
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Generate a simple Python exercise for beginners based on print statements."
            }
        ],
        temperature=0.7,
        max_completion_tokens=200,
    )
    gen_exercise = completion.choices[0].message.content
    gen_exercise = gen_exercise.split("</think>")[-1].strip()  # Remove <think> section if present
    return gen_exercise

# Streamlit UI
st.title("Python AI Learning - Lesson 1")
st.subheader("Introduction to Python")

# Section 1: Welcome Message
st.write("Welcome to your first Python lesson! Python is a powerful and beginner-friendly programming language used in web development, data science, AI, and more.")

# Section 2: First Python Program
st.write("### Your First Python Program")
st.write("To display text in Python, we use the `print()` function. Try running this:")
st.code('print("Hello, world!")', language='python')

# AI-Generated Exercise
st.write("### AI-Generated Exercise")
st.write(generate_exercise())

# User Experiment: Writing Print Statements
st.write("Now, try solving the exercise below!")
user_code = st.text_area("Write your Python code:", "")

if st.button("Run Code"):
    try:
        exec(user_code)
        st.success("✅ Your code ran successfully!")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

if st.button("Get AI Suggestion"):
    suggestion = get_ai_suggestion(user_code)
    st.write("### AI Suggestion:")
    st.markdown(suggestion)

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

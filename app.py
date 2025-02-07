import streamlit as st
from openai import OpenAI
import os
from groq import Groq
import io
import sys


client = Groq(api_key=os.getenv("GROQ_API_TOKEN"))

def generate_lesson():
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""Create an interactive Python lesson for beginners, in a funny way, including explanations and coding examples. Do not generate exercise.
                            """
            },
            {
                "role": "user",
                "content":   f"""
                            Lesson about python in general and print statement
                            """
            }
        ],
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        stream=None,
        stop=None,
    )
    

    return completion.choices[0].message.content

def get_ai_suggestion(user_input, exercise_prompt):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a helpful AI tutor for Python beginners.
                            The user is attempting to solve a Python exercise.
                            - First, check if the user's solution matches the requirements of the exercise.
                            - If the solution is correct, congratulate the user and explain why.
                            - If the solution is incorrect, provide corrections and explain the mistakes in a simple way.
                            """
            },
            {
                "role": "user",
                "content": f"""
                            Exercise: 
                            {exercise_prompt}

                            User's Code:
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
    
    return completion.choices[0].message.content
def generate_exercise():
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Generate a simple Python exercise for beginners based on print statements. Only give exercise objective and an example of output. Avoid exercise with input() "
            }
        ],
        temperature=0.7,
        max_completion_tokens=200,
    )
    #gen_exercise = completion.choices[0].message.content
    #gen_exercise = gen_exercise.split("</think>")[-1].strip()  # Remove <think> section if present
    return completion.choices[0].message.content

# Streamlit UI
st.markdown(generate_lesson())

st.subheader("AI Generated Exercise")
# Generate and store the exercise
if "exercise_prompt" not in st.session_state:
    st.session_state.exercise_prompt = generate_exercise()  # Store in session state
st.write(st.session_state.exercise_prompt)

# User Experiment: Writing Print Statements
st.write("Now, try solving the exercise below!")
user_code = st.text_area("Write your Python code:", "")

if st.button("Run Code"):
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()  # Redirect stdout to capture output
    try:
        exec(user_code, {})  # Execute user code
        output = sys.stdout.getvalue()  # Get printed output
        st.success("✅ Your code ran successfully!")
        st.code(output, language="text")  # Show output
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
    finally:
        sys.stdout = old_stdout  # Reset stdout

if st.button("Get AI Suggestion"):
    suggestion = get_ai_suggestion(user_code, st.session_state.exercise_prompt)
    st.write("### AI Suggestion:")
    st.markdown(suggestion)

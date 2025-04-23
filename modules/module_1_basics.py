import streamlit as st
from ai_helpers import generate_exercises

def run():
    st.title("Module 1: Python Basics")
    st.write("Welcome to your first Python lesson!")

    st.subheader("What is a Variable?")
    st.code("x = 5\nprint(x)")

    st.subheader("Practice Time!")
    topic = "variables"
    
    # Get full content (including solution/explanation)
    full_exercise = generate_exercises.generate_exercise(topic)

    # Split content into parts
    split_sections = full_exercise.split("Solution:")
    question = split_sections[0].strip()
    solution_and_explanation = "Solution:" + split_sections[1].strip() if len(split_sections) > 1 else ""

    # Show only the exercise first
    st.write(question)

    user_input = st.text_input("Your Answer")

    # Show solution after user submits something
    if user_input:
        with st.expander("See the suggested solution and explanation"):
            st.markdown(solution_and_explanation)

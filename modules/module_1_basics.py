import streamlit as st
from ai_helpers import generate_exercises

def run():
    st.title("🧠 Module 1: Python Basics")
    st.write("Welcome to your first Python lesson! Let's learn about **variables**.")

    st.subheader("📘 What is a Variable?")
    st.code("x = 5\nprint(x)")

    st.divider()

    st.subheader("🧪 Practice Time!")

    topic = "variables"
    full_exercise = generate_exercises.generate_exercise(topic)

    # Split question from solution
    if "Solution:" in full_exercise:
        question, solution = full_exercise.split("Solution:", 1)
    else:
        question, solution = full_exercise, ""

    st.markdown(question.strip())

    user_input = st.text_input("Your Answer", placeholder="Type your solution or notes here...")

    if user_input.strip():
        with st.expander("💡 Show Solution & Explanation"):
            st.markdown("**Solution:**")
            st.markdown(solution.strip())

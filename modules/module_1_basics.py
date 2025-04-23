import streamlit as st
from ai_helpers import generate_exercises

def run():
    st.title("Module 1: Python Basics")
    st.write("Welcome to your first Python lesson!")

    st.subheader("What is a Variable?")
    st.code("x = 5\nprint(x)")

    st.subheader("Practice Time!")

    # 👇 Choose the topic you want an exercise about
    topic = "variables"  # You can also make this dynamic with a selectbox later

    exercise_text = generate_exercises.generate_exercise(topic)
    st.write(exercise_text)

    user_input = st.text_input("Your Answer")

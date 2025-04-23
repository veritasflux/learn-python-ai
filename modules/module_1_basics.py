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
    
    # Button to generate exercise
    if "exercise_text" not in st.session_state:
        if st.button("Generate Exercise"):
            full_exercise = generate_exercises.generate_exercise(topic)
            st.session_state.exercise_text = full_exercise

    # Display the exercise once generated
    if "exercise_text" in st.session_state:
        full_exercise = st.session_state.exercise_text

        # Split question and solution
        if "Solution:" in full_exercise:
            question, solution = full_exercise.split("Solution:", 1)
        else:
            question, solution = full_exercise, ""

        st.markdown(question.strip())

        user_input = st.text_area("Your Answer", height=100)
        
        if st.button("✅ Submit"):
            st.success("Your answer has been submitted!")
            with st.expander("💡 Show Solution & Explanation"):
                st.markdown("**Solution:**")
                st.markdown(solution.strip())

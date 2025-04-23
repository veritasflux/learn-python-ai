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

    # Generate new exercise
    if "exercise_data" not in st.session_state:
        if st.button("🎲 Generate New Exercise"):
            with st.spinner("Generating exercise..."):
                exercise_data = generate_exercises.generate_exercise(topic)

                if isinstance(exercise_data, dict) and "question" in exercise_data and "solution" in exercise_data:
                    st.session_state.exercise_data = exercise_data
                    st.session_state.show_solution = False
                    st.session_state.user_input = ""
                else:
                    st.error("❌ Failed to generate a valid exercise. Please try again.")

    # Display the exercise
    if "exercise_data" in st.session_state:
        st.markdown("### 📝 Exercise")
        st.markdown(st.session_state.exercise_data["question"])

        # Code input
        st.session_state.user_input = st.text_area("✏️ Your Answer", value=st.session_state.get("user_input", ""), height=120)

        if st.button("✅ Submit Your Answer"):
            st.session_state.show_solution = True

        # Show solution and explanation
        if st.session_state.get("show_solution"):
            solution = st.session_state.exercise_data["solution"]
            st.markdown("### ✅ Solution Code")
            st.code(solution.get("code", "No code provided."))

            st.markdown("### 💡 Explanation")
            st.markdown(solution.get("explanation", "No explanation provided."))


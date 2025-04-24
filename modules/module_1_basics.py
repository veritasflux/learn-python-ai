import streamlit as st
from ai_helpers import generate_exercises, hint_generator
import io
import contextlib


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

    if "exercise_data" in st.session_state:
        st.markdown("### 📝 Exercise")
        st.markdown(st.session_state.exercise_data["question"])

        st.markdown("### ✏️ Try It Out!")
        user_code = st.text_area("Write your Python code here:", value=st.session_state.get("user_input", ""), height=180, key="user_code_input")

        # Run Code
        if st.button("🚀 Run My Code"):
            st.session_state.user_input = user_code
            st.session_state.last_run_code = user_code
        
            output_buffer = io.StringIO()
            try:
                with contextlib.redirect_stdout(output_buffer):
                    exec(user_code, {})
                st.success("✅ Code ran successfully!")
                st.markdown("**🖥️ Output:**")
                st.code(output_buffer.getvalue())
                user_code_valid = True
            except Exception as e:
                st.error("⚠️ Error in your code:")
                st.code(str(e))
                user_code_valid = False
        
        # Evaluate correctness using hint_generator
        if user_code_valid:
            with st.spinner("Evaluating your solution..."):
                user_code = st.session_state["last_run_code"]
                solution_code = st.session_state["exercise_data"]["solution"]["code"]
                hint = hint_generator.generate_hint(user_code, solution_code)
    
            if "correct" in hint.lower() and "wrong" not in hint.lower():
                st.success("🎉 Congratulations! Your solution is logically correct.")
            else:
                st.info(f"💡 Hint: {hint}")
        st.divider()

        # Reveal solution
        if st.button("💡 I Give Up! Show Solution"):
            st.session_state.show_solution = True

        if st.session_state.get("show_solution"):
            solution = st.session_state.exercise_data["solution"]
            st.markdown("### ✅ Solution Code")
            st.code(solution.get("code", "No code provided."))

            st.markdown("### 💡 Explanation")
            st.markdown(solution.get("explanation", "No explanation provided."))

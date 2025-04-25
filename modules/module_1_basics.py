import streamlit as st
from ai_helpers import generate_exercises, hint_generator
import io
import contextlib
import json

def display_intro():
    st.title("🧠 Module 1: Python Basics")
    st.write("Welcome to your first Python lesson! Let's learn about **variables**.")

    st.subheader("📘 What is a Variable?")
    st.markdown("""
    A **variable** is a way to store information in your program. Think of it as a labeled box where you can keep data.
    
    For example:
    """)
    st.code("""
    x = 5
    name = "Alice"
    price = 9.99
    """)

    st.markdown("""📌 Let's update a variable:""")
    st.code("""
    x = 5
    print("Before:", x)
    
    x = 10
    print("After:", x)
    """)

    st.info("""Common Mistake
    Don't use `=` to compare values. Use `==` for comparison.
    """, icon="💡")
    st.code("""
    x = 5    # correct: assigning value
    if x == 5:  # correct: comparing
        print("x is 5")
    """)

def display_quiz():
    st.markdown("### 🧠 Quick Quiz")
    quiz_answer = st.radio("Which line correctly assigns a value to a variable?", [
        "x == 10",
        "10 = x",
        "x = 10",
    ])
    
    if st.button("📝 Check Answer"):
        if quiz_answer == "x = 10":
            st.success("Correct! ✅")
        else:
            st.error("Oops! Remember, `=` assigns a value to a variable.")

def generate_exercise_data(module_name):
    if f"{module_name}_exercise_data" not in st.session_state:
        if st.button(f"🎲 Generate New Exercise"):
            with st.spinner("Generating exercise..."):
                exercise_data = generate_exercises.generate_exercise(module_name)
                if isinstance(exercise_data, dict) and "question" in exercise_data and "solution" in exercise_data:
                    st.session_state[f"{module_name}_exercise_data"] = exercise_data
                    st.session_state[f"{module_name}_show_solution"] = False
                    st.session_state[f"{module_name}_user_input"] = ""
                else:
                    st.error("❌ Failed to generate a valid exercise. Please try again.")

def display_exercise():
    if "exercise_data" in st.session_state:
        st.markdown("### 📝 Exercise")
        st.markdown(st.session_state.exercise_data["question"])

        st.markdown("### ✏️ Try It Out!")
        draft_code = st.text_area(
            "Write your Python code here:",
            value=st.session_state.get("user_input", ""),
            height=180,
            key="user_code_input"
        )

        # Handle running code (to be implemented in another function)
        if st.button("🚀 Run My Code"):
            execute_code(draft_code)

def execute_code(draft_code):
    st.session_state["last_run_code"] = draft_code  # Save latest version
    output_buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(output_buffer):
            exec(draft_code, {})  # Run the updated code
        st.success("✅ Code ran successfully!")
        st.markdown("**🖥️ Output:**")
        st.code(output_buffer.getvalue().strip())
        user_code_valid = True
    except Exception as e:
        st.error("⚠️ Error in your code:")
        st.code(str(e))
        user_code_valid = False

    if user_code_valid:
        evaluate_solution()

def evaluate_solution():
    solution_code = st.session_state["exercise_data"]["solution"]["code"]
    solution_output_buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(solution_output_buffer):
            exec(solution_code, {})
        expected_output = solution_output_buffer.getvalue().strip()
    except Exception as e:
        expected_output = None
        st.warning("⚠️ Could not evaluate the reference solution.")

    generate_hint(st.session_state["last_run_code"], solution_code)

def generate_hint(user_code, solution_code):
    with st.spinner("Evaluating your logic..."):
        # Call the hint generator and get feedback as JSON
        hint_json = hint_generator.generate_hint(user_code, solution_code)
        
        try:
            # Parse the response as JSON
            hint_response = json.loads(hint_json)
            is_correct = hint_response.get("is_correct", False)
            feedback = hint_response.get("feedback", "No feedback provided.")
            
            if is_correct:
                st.success("🎉 Congratulations! Your solution is logically correct.")
                st.info(f"💡 Hint: {feedback}")
            else:
                st.info(f"💡 Hint: {feedback}")
        except json.JSONDecodeError as e:
            st.warning(f"⚠️ Could not evaluate the feedback properly. Error: {str(e)}")


def display_solution():
    if st.button("💡 I Give Up! Show Solution"):
        st.session_state.show_solution = True

    if st.session_state.get("show_solution"):
        solution = st.session_state.exercise_data["solution"]
        st.markdown("### ✅ Solution Code")
        st.code(solution.get("code", "No code provided."))

        st.markdown("### 💡 Explanation")
        st.markdown(solution.get("explanation", "No explanation provided."))

def run():
    # Display all parts of the app
    display_intro()
    display_quiz()
    # Generate exercise for Variables
    generate_exercise_data("assigning variables")
    display_exercise("assigning variables")
    display_solution("assigning variables")

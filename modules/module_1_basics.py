import streamlit as st
from ai_helpers import generate_exercises, hint_generator
import io
import contextlib
import json


def run():
    st.title("🧠 Module 1: Python Basics")
    st.write("Welcome to your first Python lesson! Let's learn about **variables**.")

    st.subheader("📘 What is a Variable?")
    st.markdown("""
    A **variable** is a way to store information in your program. Think of it as a labeled box where you can keep data.
    
    For example:
    
    ```python
    x = 5
    name = "Alice"
    price = 9.99

    ---

    #### 2. **Visual Output for Variable Values**
    Show how the variable changes over time to make it more intuitive:
    
    ```python
    st.markdown("📌 Let's update a variable:")
    
    st.code("""
    x = 5
    print("Before:", x)
    
    x = 10
    print("After:", x)
    """)

    st.info("""
    💡 **Common Mistake**:
    Don't use `=` to compare values. Use `==` for comparison.
    
    ```python
    x = 5    # correct: assigning value
    if x == 5:  # correct: comparing
        print("x is 5")

    ---

    #### 4. **Add a Quick Quiz / Reflection Question**
    Introduce 1-2 short MCQs to reinforce the topic:
    
    ```python
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
    st.divider()
    st.subheader("🧪 Practice Time!")

    topic = "variables"

    # Generate exercise
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

    # Show the exercise and editor
    if "exercise_data" in st.session_state:
        st.markdown("### 📝 Exercise")
        st.markdown(st.session_state.exercise_data["question"])

        st.markdown("### ✏️ Try It Out!")
        user_code = st.text_area(
            "Write your Python code here:",
            height=180,
            key="user_code_input"
        )

        # Run and evaluate code
        if st.button("🚀 Run My Code"):
            user_code = st.session_state["user_code_input"]  # This holds the text area's content
            st.session_state.user_input = user_code
            st.session_state.last_run_code = user_code
        
            output_buffer = io.StringIO()
            try:
                with contextlib.redirect_stdout(output_buffer):
                    exec(user_code, {})
                st.success("✅ Code ran successfully!")
                user_output = output_buffer.getvalue().strip()
                st.markdown("**🖥️ Output:**")
                st.code(user_output)
                user_code_valid = True
            except Exception as e:
                st.error("⚠️ Error in your code:")
                st.code(str(e))
                user_code_valid = False
        
            if user_code_valid:
                solution_code = st.session_state["exercise_data"]["solution"]["code"]
                solution_output_buffer = io.StringIO()
                try:
                    with contextlib.redirect_stdout(solution_output_buffer):
                        exec(solution_code, {})
                    expected_output = solution_output_buffer.getvalue().strip()
                except Exception as e:
                    expected_output = None
                    st.warning("⚠️ Could not evaluate the reference solution.")
            
                with st.spinner("Evaluating your logic..."):
                    # Call the hint generator and get feedback as JSON
                    hint_json = hint_generator.generate_hint(user_code, solution_code)

                    try:
                        # Parse the response as JSON
                        hint_response = json.loads(hint_json)
                        print(hint_response)
                        is_correct = hint_response.get("is_correct", False)
                        feedback = hint_response.get("feedback", "No feedback provided.")
                        
                        if is_correct:
                            st.success("🎉 Congratulations! Your solution is logically correct.")
                            st.info(f"💡 Hint: {feedback}")
                        else:
                            st.info(f"💡 Hint: {feedback}")
                    except json.JSONDecodeError:
                        st.warning("⚠️ Could not evaluate the feedback properly.")

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

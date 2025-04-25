import streamlit as st
from ai_helpers import generate_exercises, hint_generator
import io
import contextlib
import json

def display_intro():
    st.title("🧠 Module 2: Core Data Types")
    st.write("Welcome to the second lesson on **Python Basics**! In this lesson, we will explore **Core Data Types**: Numbers, Text, and Truth Values.")

    st.subheader("📘 Core Data Types Overview")
    st.markdown("""
    Python has a variety of built-in **core data types** that allow us to work with different kinds of data:
    
    - **Numbers** (integers and floats)
    - **Text** (strings)
    - **Truth Values** (booleans)
    
    These are fundamental to all programs. Let's dive into each type!
    """)

def display_numbers():
    st.subheader("🔢 Numbers: Integers and Floats")

    st.markdown("""
    **Integers (`int`)** are whole numbers, such as `5`, `-3`, or `0`. These are used for counting or indexing.
    
    **Floats (`float`)** are numbers that can have a decimal point, such as `3.14`, `-0.001`, or `2.0`.
    
    Here's how we use them:
    """)

    st.code("""
    # Example with Integers
    age = 25
    count = 10
    
    # Example with Floats
    pi = 3.14
    temperature = -5.7
    """)

    st.markdown("You can perform operations on numbers like addition, subtraction, multiplication, and division:")

    st.code("""
    sum_result = age + count  # Integer addition
    area = pi * 5 ** 2  # Calculating area of a circle with radius 5
    """)

def display_text():
    st.subheader("📝 Text: Strings (`str`)")

    st.markdown("""
    **Strings (`str`)** represent sequences of characters. Strings are used for text manipulation and storing names, sentences, etc.
    
    Example strings: `"hello"`, `"Python"`, `'123'`.

    Strings can be created using either single quotes `'` or double quotes `"`.

    Here's how to create and manipulate strings:
    """)

    st.code("""
    # Creating Strings
    name = "Alice"
    greeting = 'Hello, ' + name  # Concatenating strings
    
    # String Methods
    uppercase_name = name.upper()  # Convert string to uppercase
    length_of_name = len(name)  # Get the length of the string
    """)

    st.markdown("You can use string methods like `.lower()`, `.replace()`, `.strip()`, etc., to modify and manipulate text.")

def display_booleans():
    st.subheader("✅ Truth Values: Booleans (`bool`)")

    st.markdown("""
    **Booleans (`bool`)** represent logical values: either `True` or `False`. They are useful for making decisions in your program.
    
    Booleans are used in conditional statements (like `if` statements) to control the flow of a program.

    Here's an example of using booleans:
    """)

    st.code("""
    is_raining = True
    if is_raining:
        print("Take an umbrella!")
    else:
        print("No umbrella needed!")
    """)

def display_quiz():
    st.markdown("### 🧠 Quick Quiz")
    quiz_answer = st.radio("Which of the following is a valid integer?", [
        "3.14",
        "-10.5",
        "25",
    ])

    if st.button("📝 Check Answer"):
        if quiz_answer == "25":
            st.success("Correct! ✅")
        else:
            st.error("Oops! Remember, an integer is a whole number without a decimal.")

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
                    
def display_exercise(module_name):
    if f"{module_name}_exercise_data" in st.session_state:
        st.markdown("### 📝 Exercise")
        st.markdown(st.session_state[f"{module_name}_exercise_data"]["question"])

        st.markdown("### ✏️ Try It Out!")
        draft_code = st.text_area(
            "Write your Python code here:",
            value=st.session_state.get(f"{module_name}_user_input", ""),
            height=180,
            key=f"{module_name}_user_code_input"
        )

        # Handle running code (to be implemented in another function)
        if st.button("🚀 Run My Code"):
            execute_code(module_name,draft_code)

def execute_code(module_name,draft_code):
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
        evaluate_solution(module_name)

def evaluate_solution(module_name):
    solution_code = st.session_state[f"{module_name}_exercise_data"]["solution"]["code"]
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

def display_solution(module_name):
    if st.button("💡 I Give Up! Show Solution"):
        st.session_state[f"{module_name}_show_solution"] = True

    if st.session_state.get(f"{module_name}_show_solution"):
        solution = st.session_state[f"{module_name}_exercise_data"]["solution"]
        st.markdown("### ✅ Solution Code")
        st.code(solution.get("code", "No code provided."))

        st.markdown("### 💡 Explanation")
        st.markdown(solution.get("explanation", "No explanation provided."))

def run():
    # Display all parts of the app
    display_intro()
    display_numbers()
    display_text()
    display_booleans()
    display_quiz()
    
    # Generate exercise for Core Data Types
    generate_exercise_data("core_data_types_string_integers_floats_booleans")
    display_exercise("core_data_types_string_integers_floats_booleans")
    display_solution("core_data_types_string_integers_floats_booleans")
    

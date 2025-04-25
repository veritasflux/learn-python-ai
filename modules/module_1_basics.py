import streamlit as st
from ai_helpers import generate_exercises, hint_generator, generate_slide_explanation, tts_helper
import io
import contextlib
import json
import base64

slides = [
    {
        "title": "🧠 Module 1: Python Basics",
        "content": """
Welcome to your first Python lesson! Let's learn about **variables**.

A **variable** is a way to store information in your program. Think of it as a labeled box where you can keep data.
""",
    },
    {
        "title": "📦 Examples of Variables",
        "content": """```python
x = 5
name = "Alice"
price = 9.99
```""",
    },
    {
        "title": "🔁 Updating a Variable",
        "content": """```python
x = 5
print("Before:", x)

x = 10
print("After:", x)
```""",
    },
    {
        "title": "💡 Common Mistake",
        "content": """
Don't use `=` to compare values. Use `==` for comparison.

```python
x = 5    # correct: assigning value
if x == 5:  # correct: comparing
    print("x is 5")
```""",
    },
    {
        "title": "🧠 Quick Quiz",
        "content": None  # Will display with a function
    }
]

# Cache the explanations in a dictionary
cached_explanations = {}

def fetch_and_cache_explanations():
    """
    Fetches all slide explanations at the start of the lesson and caches them.
    """
    global cached_explanations
    cached_explanations = generate_slide_explanation.fetch_slide_explanations(slides)

def display_slide(index):
    """
    Display the content and explanation of a specific slide.
    """
    if 0 <= index < len(slides):
        slide = slides[index]
        st.subheader(slide["title"])
        if slide["content"]:
            st.markdown(slide["content"])
            # Get the explanation from the cache
            explanation = cached_explanations.get(f"Slide {index+1}", "No explanation available.")
            st.markdown(f"### 📝 Detailed Explanation\n{explanation}")
            
            # Add a button to trigger TTS and play the explanation
            if st.button(f"🔊 Read Slide {index + 1}"):
                st.info("Generating audio...")
                
                # Generate speech from the explanation and save it as a file
                file_path = tts_helper.text_to_speech(explanation, filename=f"slide_{index}.wav")
                
                # Read the generated audio file and play it
                audio_bytes = open(file_path, 'rb').read()
                st.audio(audio_bytes, format="audio/wav")
        elif slide["title"] == "🧠 Quick Quiz":
            display_quiz()
            
def slide_controls():
    if "slide_index" not in st.session_state:
        st.session_state.slide_index = 0

    cols = st.columns([1, 5, 1])

    # Read current index
    current_index = st.session_state.slide_index

    # Back button
    if cols[0].button("⬅️ Back") and current_index > 0:
        current_index -= 1

    # Next button
    if cols[2].button("Next ➡️") and current_index < len(slides) - 1:
        current_index += 1

    # Update session state
    st.session_state.slide_index = current_index

    # Display slide info and content
    with cols[1]:
        st.markdown(f"#### Slide {current_index + 1} of {len(slides)}")

    display_slide(current_index)

def display_quiz():
    quiz_answer = st.radio("Which line correctly assigns a value to a variable?", [
        "x == 10",
        "10 = x",
        "x = 10",
    ], key="quiz_radio")
    
    if st.button("📝 Check Answer", key="check_quiz_answer"):
        if quiz_answer == "x = 10":
            st.success("Correct! ✅")
        else:
            st.error("Oops! Remember, `=` assigns a value to a variable.")

# Keep the rest of your logic the same
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

        if st.button("🚀 Run My Code"):
            execute_code(draft_code, module_name)

def execute_code(draft_code, module_name):
    st.session_state["last_run_code"] = draft_code
    output_buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(output_buffer):
            exec(draft_code, {})
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
        hint_json = hint_generator.generate_hint(user_code, solution_code)
        try:
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
    if f"{module_name}_exercise_data" not in st.session_state:
        st.warning(f"⚠️ Exercise data for {module_name} not found. Please generate the exercise first.")
        return

    if st.button("💡 I Give Up! Show Solution"):
        st.session_state[f"{module_name}_show_solution"] = True

    if st.session_state.get(f"{module_name}_show_solution"):
        solution = st.session_state[f"{module_name}_exercise_data"]["solution"]
        st.markdown("### ✅ Solution Code")
        st.code(solution.get("code", "No code provided."))

        st.markdown("### 💡 Explanation")
        st.markdown(solution.get("explanation", "No explanation provided."))

def run():
    module_name = "assigning variables"
    slide_controls()
    st.divider()
    fetch_and_cache_explanations()

    # Only show exercises after the final slide
    if st.session_state.slide_index == len(slides) - 1:
        generate_exercise_data(module_name)
        display_exercise(module_name)
        display_solution(module_name)


import streamlit as st
from modules import module_1_basics, module_1_cores

# Sidebar for Module and Lesson selection
st.sidebar.title("Python Learning Platform")

# Define a dictionary for Modules and their respective lessons
modules = {
    "Module 1: Python's Basic Language (The Alphabet & Words)": [
        ("Variables", module_1_basics.run),
        ("Core Data Types", module_1_cores.run),
    ]
}

# Select the module
module = st.sidebar.radio("Choose a Module", list(modules.keys()))

# Display lessons for the selected module
lesson_name = st.sidebar.radio("Choose a Lesson", [lesson[0] for lesson in modules[module]])

# Run the corresponding lesson
for lesson in modules[module]:
    if lesson[0] == lesson_name:
        lesson[1]()  # Call the function that runs the lesson

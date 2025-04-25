
import streamlit as st
from modules import module_1_basics, module_1_cores

st.sidebar.title("Python Learning Platform")
module = st.sidebar.radio("Choose a Module", [
    "Module 1: Basics",
    "Module 1: Cores",
])

if module == "Module 1: Basics":
    module_1_basics.run()
if module == "Module 1: Cores":
    module_1_cores.run()

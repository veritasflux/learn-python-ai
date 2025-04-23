
import streamlit as st
from modules import module_1_basics

st.sidebar.title("Python Learning Platform")
module = st.sidebar.radio("Choose a Module", [
    "Module 1: Basics",
])

if module == "Module 1: Basics":
    module_1_basics.run()

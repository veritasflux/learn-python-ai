import streamlit as st
from transformers import pipeline
def get_ai_suggestion(user_input):
    generator = pipeline("text2text-generation", model="google/flan-t5-small")
    response = generator(f"Correct this Python code: {user_input}", max_length=50)
    return response[0]['generated_text']

# Streamlit UI
st.title("Python AI Learning - Lesson 1")
st.subheader("Introduction to Python")

st.write("Python is a popular programming language. Let's start with a simple command:")
st.code('print("Hello, world!")', language='python')

st.write("Try writing your own code below:")
user_code = st.text_area("Write Python code:", "print(")

if st.button("Get AI Suggestion"):
    suggestion = get_ai_suggestion(user_code)
    st.write("### AI Suggestion:")
    st.code(suggestion, language='python')

st.write("### AI-Powered Help")
st.write("💡 If you're stuck, the AI will suggest corrections!")

import streamlit as st
import requests
import os

API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
headers = {"Authorization": "Bearer " + os.getenv("HUGGING_API_KEY")}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Streamlit UI
st.title("Python AI Learning - Lesson 1")
st.subheader("Introduction to Python")

st.write("Python is a popular programming language. Let's start with a simple command:")
st.code('print("Hello, world!")', language='python')

st.write("Try writing your own code below:")
user_code = st.text_area("Write Python code:", "print(")

if st.button("Get AI Suggestion"):
    payload = {"inputs" : "Complete with simple example python code :" user_code}
    response = query(payload)
    
    # Extract the response correctly
    if isinstance(response, list) and "generated_text" in response[0]:
        suggestion = response[0]["generated_text"]
    else:
        suggestion = "Error: Unable to generate text"

    st.write("### AI Suggestion:")
    st.code(suggestion, language='python')

st.write("### AI-Powered Help")
st.write("💡 If you're stuck, the AI will suggest corrections!")

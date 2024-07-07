import google.generativeai as genai
import os
import time
import re
import streamlit as st
genai.configure(api_key="AIzaSyCD6M571IvBJHm31wTF5vOrGV60gk-PtRQ")
model = genai.GenerativeModel('gemini-1.5-flash')

def stream_data(data, delay: float = 0.02):
    words = re.split(r'[ *]', data)
    for word in words:
        st.text(word + " ", end='', flush=True)
        time.sleep(delay)
    st.text()  
    
def chatResponse(user_input):
    #user_input = input("Enter prompt: ")
    response = model.generate_content(user_input)
    return response


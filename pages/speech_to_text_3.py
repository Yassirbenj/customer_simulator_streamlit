import speech_recognition as sr
import streamlit as st

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    st.write("Say something!")
    audio = r.listen(source)

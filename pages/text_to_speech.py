import streamlit as st
from gtts import gTTS
import tempfile

def tts(text):
    tts_response = gTTS(text, lang="en", slow=False)
    st.audio(tts_response, format="audio/mp3", start_time=0)


tts("My name is yassir")

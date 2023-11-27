import streamlit as st
from gtts import gTTS
import tempfile

def tts(text):
    tts_response = gTTS(text, lang="en", slow=False)
    if tts_response:
        my_file_name = text[0:20]
        tts.save(f"temp/{my_file_name}.mp3")
        audio_file = open(f"temp/{my_file_name}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown("Customer talking:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)


tts("My name is yassir")

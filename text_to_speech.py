import streamlit as st
from gtts import gTTS

def tts(text):
    tts = gTTS(text, lang="en", slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    audio_file = open(f"temp/{my_file_name}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown("Customer talking:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

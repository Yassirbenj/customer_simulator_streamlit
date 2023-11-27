import streamlit as st
from gtts import gTTS
import tempfile

def tts(text):
    tts_response = gTTS(text, lang="en", slow=False)
    if tts_response:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(tts_response)
            temp_audio_filename = temp_audio_file.name

        audio_bytes = temp_audio_filename.read()
        st.markdown("Customer talking:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

input=st.text_input("Text")
tts(input)

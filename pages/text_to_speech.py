import streamlit as st
from gtts import gTTS
import tempfile
import os

def tts(text):
    # Create a temporary file to save the audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_filepath = temp_audio.name

        # Generate gTTS audio and save it to the temporary file
        tts_response = gTTS(text, lang="en", slow=False)
        tts_response.save(temp_filepath)

        # Display the audio using st.audio
        st.audio(temp_filepath, format="audio/mp3", start_time=0)

    # Delete the temporary file after displaying
    os.remove(temp_filepath)

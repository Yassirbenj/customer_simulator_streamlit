import streamlit as st
import pyttsx3
import tempfile
import os

import base64




def tts(text,rate,volume):
    converter = pyttsx3.init()
    # Sets speed percent
    # Can be more than 100
    converter.setProperty('rate', rate)
    # Set volume 0-1
    converter.setProperty('volume', volume)
    # Create a temporary file to save the audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_filepath = temp_audio.name

        converter.say("Hello GeeksforGeeks")

        # Display the audio using st.audio
        st.audio(temp_filepath, format="audio/mp3", start_time=0)

    # Delete the temporary file after displaying
    os.remove(temp_filepath)

rate=st.number_input("rate")
volume=st.number_input("volume")
text=st.text_input("text")
tts(text,rate,volume)

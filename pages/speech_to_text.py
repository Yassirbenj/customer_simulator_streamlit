import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai
import speech_recognition as sr
import io

r = sr.Recognizer()


openai_api_key = st.secrets["openai"]

audio_bytes = audio_recorder(energy_threshold=0.01,pause_threshold=2)

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    # Convert bytes to a file-like object
    audio_file = io.BytesIO(audio_bytes)

    transcript = openai.Audio.transcribe(model="whisper-1", file=audio_file, api_key=openai_api_key)
    st.write(transcript.text)

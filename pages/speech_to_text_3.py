import speech_recognition as sr
import streamlit as st
from audio_recorder_streamlit import audio_recorder

openai_api_key = st.secrets["openai"]

audio_bytes = audio_recorder(energy_threshold=0.01, pause_threshold=2)

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(audio_bytes) as source:
    audio = r.record(source)  # read the entire audio file

if audio_bytes:
    # recognize speech using Whisper API
    try:
        st.write(f"Whisper API thinks you said {r.recognize_whisper_api(audio_bytes, api_key=openai_api_key)}")
    except sr.RequestError as e:
        st.write("Could not request results from Whisper API")

import speech_recognition as sr
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import tempfile

openai_api_key = st.secrets["openai"]

audio_bytes = audio_recorder(energy_threshold=0.01, pause_threshold=2)

if audio_bytes:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        temp_audio_file.write(audio_bytes)
        temp_audio_filename = temp_audio_file.name
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(temp_audio_filename) as source:
        audio = r.record(source)  # read the entire audio file
    # recognize speech using Whisper API
    try:
        st.write(f"Transcript: {r.recognize_whisper_api(audio, api_key=openai_api_key)}")
    except sr.RequestError as e:
        st.write("Could not request results from Whisper API")
    st.audio(audio_bytes, format="audio/wav")

#if audio_bytes:
    # recognize speech using Whisper API
    #try:
    #    st.write(f"Whisper API thinks you said {r.recognize_whisper_api(audio_bytes, api_key=openai_api_key)}")
    #except sr.RequestError as e:
    #    st.write("Could not request results from Whisper API")

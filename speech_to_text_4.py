import speech_recognition as sr
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import tempfile

def stxt(key):

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
                response=r.recognize_whisper_api(audio, api_key=key)
                #st.write(f"Transcript: {response}")
            except sr.RequestError as e:
                response="Could not request results from Whisper API"
                #st.write(response)
        return response

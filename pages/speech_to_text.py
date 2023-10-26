import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai
import speech_recognition as sr
import io
import tempfile

r = sr.Recognizer()

openai_api_key = st.secrets["openai"]

audio_bytes = audio_recorder(energy_threshold=0.01, pause_threshold=2)

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    # Create a temporary WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        temp_wav.write(audio_bytes)

    # Get the filename of the temporary WAV file
    wav_filename = temp_wav.name

    # Transcribe using OpenAI
    transcript = openai.Audio.transcribe(model="whisper-1", file=wav_filename, api_key=openai_api_key)
    st.write(transcript.text)

    # Close and remove the temporary file
    temp_wav.close()

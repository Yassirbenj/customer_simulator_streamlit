import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai
import speech_recognition as sr
import tempfile
from pydub import AudioSegment

r = sr.Recognizer()

openai_api_key = st.secrets["openai"]

audio_bytes = audio_recorder(energy_threshold=0.01, pause_threshold=2)

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    # Create a temporary WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        temp_wav.write(audio_bytes)
        audio = AudioSegment.from_wav(temp_wav.name)
        temp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        audio.export(temp_mp3.name, format="mp3")
        transcript = openai.Audio.transcribe(model="whisper-1", file=temp_mp3, api_key=openai_api_key)
        st.write(transcript.text)

    # Get the filename of the temporary WAV file
    #wav_filename = temp_wav.name

    # Transcribe using OpenAI


    # Close and remove the temporary file
    temp_wav.close()
    temp_mp3.close()

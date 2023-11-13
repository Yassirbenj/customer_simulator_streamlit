# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

import assemblyai as aai
import streamlit as st
from audio_recorder_streamlit import audio_recorder

audio_bytes = audio_recorder(energy_threshold=3500, pause_threshold=2)

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

def transcript():
    aai.settings.api_key = "2ad5176bc2c74bbf9872e42f6feb357c"
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/news.mp4")
    # transcript = transcriber.transcribe("./my-local-audio-file.wav")

    st.write(transcript.text)

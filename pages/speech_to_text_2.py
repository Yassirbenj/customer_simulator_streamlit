# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

from io import BytesIO
import assemblyai as aai
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from pydub import AudioSegment
import tempfile

def convert_to_mp3(audio_bytes):
    # Load the WAV audio using pydub
    audio_segment = AudioSegment.from_wav(BytesIO(audio_bytes))

    # Save it as an MP3 file using the audio_recorder library
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_mp3:
        temp_mp3_name = temp_mp3.name
        audio_segment.export(temp_mp3_name, format="mp3")

    # Read the MP3 file as bytes
    with open(temp_mp3_name, "rb") as mp3_file:
        mp3_bytes = mp3_file.read()

    return mp3_bytes

audio_bytes = audio_recorder(energy_threshold=0.01, pause_threshold=2)

def transcript(file):
    aai.settings.api_key = "2ad5176bc2c74bbf9872e42f6feb357c"
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(file)
    st.write(transcript.text)

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    mp3_bytes = convert_to_mp3(audio_bytes)
    transcript(mp3_bytes)

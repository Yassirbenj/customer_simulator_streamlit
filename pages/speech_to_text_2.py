# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

from io import BytesIO
import assemblyai as aai
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from pydub import AudioSegment


def convert_to_mp3(audio_bytes):
    audio_segment = AudioSegment.from_wav(BytesIO(audio_bytes))
    mp3_bytes = audio_segment.export(format="mp3").read()
    return mp3_bytes

audio_bytes = audio_recorder(energy_threshold=0.01, pause_threshold=2)

def transcript(file):
    aai.settings.api_key = "2ad5176bc2c74bbf9872e42f6feb357c"
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(file)
    # transcript = transcriber.transcribe("./my-local-audio-file.wav")

    st.write(transcript.text)

if audio_bytes:
    #st.write(audio_bytes)
    st.audio(audio_bytes, format="audio/wav")
    #mp3_bytes = convert_to_mp3(audio_bytes)
    #transcript(mp3_bytes)

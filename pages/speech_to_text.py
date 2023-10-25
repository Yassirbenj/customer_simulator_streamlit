import openai
import streamlit as st
from audio_recorder_streamlit import audio_recorder

audio_bytes = audio_recorder()
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

#audio_file= open("/path/to/file/audio.mp3", "rb")
#transcript = openai.Audio.transcribe("whisper-1", audio_file)

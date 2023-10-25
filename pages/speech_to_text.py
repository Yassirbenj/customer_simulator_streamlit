import streamlit as st
from audio_recorder_streamlit import audio_recorder

audio_bytes = audio_recorder(energy_threshold=0.8,pause_threshold=2)
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

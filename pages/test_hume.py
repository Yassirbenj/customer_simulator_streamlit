import streamlit as st
import tempfile
from audio_recorder_streamlit import audio_recorder
import asyncio
from hume import HumeStreamClient, StreamSocket
from hume.models.config import ProsodyConfig

hume_key=st.secrets["hume"]


async def main():
    audio_bytes = audio_recorder(energy_threshold=0.01, pause_threshold=2,text="You start talking")

    if audio_bytes:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(audio_bytes)
            temp_audio_filename = temp_audio_file.name
        client = HumeStreamClient(hume_key)
        config = ProsodyConfig()
        async with client.connect([config]) as socket:
            result = await socket.send_file(temp_audio_filename)
            st.write(result)

asyncio.run(main())

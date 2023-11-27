import streamlit as st
import tempfile
from audio_recorder_streamlit import audio_recorder

from hume import HumeBatchClient
from hume.models.config import ProsodyConfig

import pandas as pd

hume_key=st.secrets["hume"]


def hume_prosody():
    audio_bytes = audio_recorder(energy_threshold=0.01, pause_threshold=2,text="You start talking")

    if audio_bytes:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(audio_bytes)
            temp_audio_filename = temp_audio_file.name
            filepaths = [temp_audio_filename]
            st.audio(audio_bytes,format="audio/wav")
            client = HumeBatchClient(hume_key)
            config = ProsodyConfig(granularity="conversational_turn")
            job = client.submit_job(None, [config], files=filepaths)
            st.write(job)
            st.write ("Running...")
            details = job.await_complete()
            #job.download_predictions("predictions.json")
            #st.write("Predictions downloaded to predictions.json")
            pred=job.get_predictions()
            st.write(pred)
            df=pd.read_json(pred[0].results.predictions[0].models.prosody.grouped_predictions.predictions[0].emotions)
            st.dataframe(df)

hume_prosody()

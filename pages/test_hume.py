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
            df=json_norm(pred)
            st.dataframe(df)

def json_norm(json_data):
    data = []
    for item in json_data:
        filename = item["source"]["filename"]
        predictions = item["results"]["predictions"]

        for prediction in predictions:
            text = prediction["predictions"][0]["text"]
            time_begin = prediction["predictions"][0]["time"]["begin"]
            time_end = prediction["predictions"][0]["time"]["end"]

            emotions = prediction["predictions"][0]["emotions"]
            emotion_data = {emotion["name"]: emotion["score"] for emotion in emotions}

            data.append({
                "Filename": filename,
                "Text": text,
                "Time_Begin": time_begin,
                "Time_End": time_end,
                **emotion_data
            })

    # Create DataFrame
    df = pd.DataFrame(data)
    return df


hume_prosody()

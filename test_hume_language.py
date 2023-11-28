import streamlit as st
import tempfile
from audio_recorder_streamlit import audio_recorder

from hume import HumeBatchClient
from hume.models.config import LanguageConfig
import speech_recognition as sr

import pandas as pd

hume_key=st.secrets["hume"]
key=st.secrets["openai"]


def hume_prosody():
    audio_bytes = audio_recorder(energy_threshold=(-1.0, 1.0),pause_threshold=10.0,text="You start talking 10s")

    if audio_bytes:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(audio_bytes)
            temp_audio_filename = temp_audio_file.name
            # use the audio file as the audio source
            r = sr.Recognizer()
            with sr.AudioFile(temp_audio_filename) as source:
                audio = r.record(source)  # read the entire audio file
            # recognize speech using Whisper API
                try:
                    response=r.recognize_whisper_api(audio, api_key=key)
                except sr.RequestError as e:
                    response="Could not request results from Whisper API"
                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_txt_file:
                    temp_txt_file.write(response)
                    temp_txt_filename = temp_txt_file.name
                    filepaths = [temp_txt_filename]
                    client = HumeBatchClient(hume_key)
                    config = LanguageConfig()
                    job = client.submit_job(None, [config], files=filepaths)
                    st.write(job)
                    st.write ("Running...")
                    details = job.await_complete()
                    pred=job.get_predictions()
                    st.write(pred)
                    #df=json_norm(pred)
                    #st.dataframe(df)

def json_norm(json_data):
    data=[]
    df0=pd.json_normalize(json_data)
    df1=pd.json_normalize(df0["results.predictions"][0])
    df2=pd.json_normalize(df1["models.prosody.grouped_predictions"][0])
    df3=pd.json_normalize(df2["predictions"][0])
    df4=pd.json_normalize(df3["emotions"][0])
    df4.sort_values(by="score",ascending=False,inplace=True)
    df5=df4.iloc[:5,:]
    return df5



hume_prosody()

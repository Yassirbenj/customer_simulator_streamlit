import streamlit as st
import pandas as pd

def main():
    scoring_eval()


def scoring_eval():
    uploaded_file = st.file_uploader("upload a evaluation grid file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

main()

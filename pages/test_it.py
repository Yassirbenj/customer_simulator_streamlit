import streamlit as st



def main():
    field=st.text_input("enter an evaluation  field")
    level=st.selectbox(options=["Beginner,Intermediate,Expert"])
    if field is not None & level is not None:
        start=st.button("start")

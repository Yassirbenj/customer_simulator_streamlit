import streamlit as st

st.header("test")

def main():
    field=st.text_input("enter an evaluation  field")
    level=st.selectbox("enter level of expertise",options=("Beginner,Intermediate,Expert"))
    if field is not None & level is not None:
        start=st.button("start")

main()

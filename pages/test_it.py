import streamlit as st

st.header("test")
st.session_state.status="non started"

def main():
    if st.session_state.status=="non started":
        placeholder=st.empty()
        with placeholder.container():
            field=st.text_input("enter an evaluation  field")
            level=st.selectbox("enter level of expertise",options=("Beginner,Intermediate,Expert"))
            start=st.button("start")
            if start:
                st.session_state.status="started"
                placeholder.empty()

    st.write("continue")

main()

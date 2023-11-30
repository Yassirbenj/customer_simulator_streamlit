import nltk
import streamlit as st

discussion=st.text_area("input your paragraph")
if discussion:
    words=nltk.word_tokenize(discussion)
    st.title("list of words")
    st.write(words)
    st.title("Number of words")
    st.write(len(words))

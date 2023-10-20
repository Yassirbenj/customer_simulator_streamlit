import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader

def main():
    load_dotenv()
    kb=st.file_uploader('upload your knowledgebase pdf')

    if kb is not None:
        kb_reader=PdfReader(kb)

main()

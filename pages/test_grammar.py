from gingerit.gingerit import GingerIt
import streamlit as st

text=st.input("enter a text with grammar errors")
parser = GingerIt()
st.write(parser.parse(text))

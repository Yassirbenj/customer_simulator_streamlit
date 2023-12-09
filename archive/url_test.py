
import requests
from bs4 import BeautifulSoup
import re
import streamlit as st

# What does our URL look like?
url = "https://en.wikipedia.org/wiki/Ed_Sheeran"
# Get the response
response = requests.get(url)
# Turn it into Soup
soup = BeautifulSoup(response.text, "html.parser")
# Find the right tag
life_info = soup.find("span", style= "display:none")

st.write(soup)

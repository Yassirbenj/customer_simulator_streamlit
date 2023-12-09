from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import BeautifulSoupTransformer
import streamlit as st

# Load HTML
loader = AsyncChromiumLoader(["https://www.wsj.com"])
html = loader.load()
# Transform
bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["span"])
# Result
docs_transformed[0].page_content[0:500]

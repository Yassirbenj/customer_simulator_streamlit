
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
#import os
#from dotenv import load_dotenv
import streamlit as st
from streamlit_chat import message
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

#from langchain.output_parsers import PydanticOutputParser
#from pydantic import BaseModel, Field, validator
#from typing import List

#openapi_key=os.environ.get("OPENAI_API_KEY")



def recap():
    discussion=st.text_area("enter discussion")
    start=st.button("start")
    if start:
        openai_api_key = st.secrets["openai"]
        llm=OpenAI(openai_api_key=openai_api_key)
        template = """Question: summarize the discussion between customer and sales person based on following discussion {question} """
        prompt = PromptTemplate(template=template, input_variables=["question"])
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        response=llm_chain.run(discussion)
        st.title("Recap of the discussion")
        st.write(response)
        return response


#def reset_conversation():
    #st.write(st.session_state.messages)
    #st.write(st.session_state.messages[0])
    #st.session_state.messages = st.session_state.messages[0]
    #main()


recap()

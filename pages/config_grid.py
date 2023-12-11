import streamlit as st
import pandas as pd
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain



def scoring(discussion):
    uploaded_file = st.file_uploader("upload a evaluation grid file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        eval_list=df.iloc[:,0].tolist()
        openai_api_key = st.secrets["openai"]
        llm=OpenAI(openai_api_key=openai_api_key)
        template = """Question: evaluating a discussion between a sales person and a customer based on following discussion {discussion}. give a feedback to the sales person on the good points and the major point to be improved based on the following evaluation parameters {grid} """
        prompt = PromptTemplate(template=template, input_variables=["discussion","grid"])
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        input_list = {"discussion": discussion,"grid": eval_list}
        response=llm_chain.run(input_list)
        st.title("Evaluation of the discussion")
        st.write(response)
        return response


def scoring_eval():
    uploaded_file = st.file_uploader("upload a evaluation grid file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        eval_list=df.iloc[:,0].tolist()
        #st.write(eval_list)
        return eval_list

discussion=st.file_uploader("upload discussion")
if discussion is not None:
    file_contents = discussion.read()
    decoded_discussion = file_contents.decode('utf-8')
    scoring(discussion)

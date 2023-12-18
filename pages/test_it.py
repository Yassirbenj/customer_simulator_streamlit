import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI


st.header("test")
st.session_state.status="non started"

def main():
    if st.session_state.status=="non started":
        field=st.text_input("enter an evaluation  field")
        level=st.selectbox("enter level of expertise",options=("Beginner","Intermediate","Expert"))
        start=st.button("start")
        if start:
            st.session_state.status="started"
            #main()

    if st.session_state.status=="started":
        personae(field,level)

def personae(field,level):
    context="You are recruiter asking questions to evaluate competencies of a candidate. "
    context+=f"ask a multiple choice question to evaluate competency {field} with a level of expertise {level}"
    key=st.secrets["openai"]
    llm=OpenAI(openai_api_key=key)
    template = """Question: You are recruiter asking questions to evaluate competencies of a candidate. ask a multiple choice question to evaluate competency {field} with a level of expertise {level}"""
    prompt = PromptTemplate(template=template, input_variables=["field","level"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    input_list = {"field": field,"level": level}
    question=llm_chain(input_list)
    st.write(question.text)


main()

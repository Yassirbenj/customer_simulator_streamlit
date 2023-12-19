import streamlit as st
import json

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI

from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field, validator


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
    template = """Question: You are recruiter asking questions to evaluate competencies of a candidate. ask a multiple choice question to evaluate competency {field} with a level of expertise {level}. write the question in a line and each option in a separate line. write the correct answer in a separate line"""
    prompt = PromptTemplate(template=template, input_variables=["field","level"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    input_list = {"field": field,"level": level}
    question=llm_chain(input_list)
    st.write(question["text"])

def parser (field,level):
    key=st.secrets["openai"]
    model = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.5,openai_api_key=key)

    # Defining data structure.
    class Question(BaseModel):
        setup: str = Field(description="question to evaluate a candidate including a code snippet if exists")
        #additional: str=Field(description="the snippet of the code if the question include a code.")
        options: str=Field(description="possible options for the question asked")
        answer: str = Field(description="correct answer to resolve the question")

        # validation logic
        #@validator("setup")
        #def question_ends_with_question_mark(cls, field):
        #    if field[-1] != "?":
        #        raise ValueError("Badly formed question!")
        #    return field

    # Set up a parser + inject instructions into the prompt template.
    parser = PydanticOutputParser(pydantic_object=Question)

    prompt = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    # And a query intended to prompt a language model to populate the data structure.
    prompt_and_model = prompt | model
    query=f"A question to evaluate competency of a candidate in field {field} with a level of expertise {level}"
    input_data = {
        "query": query,
        "setup": "Your setup question here",  # Provide the setup question
        #"additional": "Your additional informations about the question here",
        "options": "Your options here",  # Provide the options for the question
        "answer": "Your correct answer here",  # Provide the correct answer
    }

    output = prompt_and_model.invoke(input_data)
    #st.write(output)
    output_dict = json.loads(output)
    st.write(output_dict)
    question=output_dict["setup"]
    options=output_dict["options"]
    answer=output_dict["answer"]
    st.header("Question")
    st.write(question)
    st.header("Options")
    st.write(options)

    #response=parser.invoke(output)
    #st.write(response)

def parser2 (field,level):
    key=st.secrets["openai"]
    llm=OpenAI(openai_api_key=key)
    template = """Question: You are recruiter asking a question to evaluate competencies of a candidate on competency {field} with a level of expertise {level}."""
    prompt = PromptTemplate(template=template, input_variables=["field","level"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    input_list = {"field": field,"level": level}
    question=llm_chain(input_list)
    st.write(question["text"])

    model = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.5,openai_api_key=key)

    # Defining data structure.
    class Question(BaseModel):
        #setup: str = Field(description="question to evaluate a candidate including a code snippet if exists")
        #additional: str=Field(description="the snippet of the code if the question include a code.")
        options: str=Field(description="possible options for the question asked")
        answer: str = Field(description="correct answer to resolve the question")

        # validation logic
        #@validator("setup")
        #def question_ends_with_question_mark(cls, field):
        #    if field[-1] != "?":
        #        raise ValueError("Badly formed question!")
        #    return field

    # Set up a parser + inject instructions into the prompt template.
    parser = PydanticOutputParser(pydantic_object=Question)

    prompt = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    # And a query intended to prompt a language model to populate the data structure.
    prompt_and_model = prompt | model
    query=f"You want to evaluate competencies of a candidate. Give three options to respond to question {question}. Only one option should be valid."
    input_data = {
        "query": query,
        #"setup": "Your setup question here",  # Provide the setup question
        #"additional": "Your additional informations about the question here",
        "options": "Your options here",  # Provide the options for the question
        "answer": "Your correct answer here",  # Provide the correct answer
    }

    output = prompt_and_model.invoke(input_data)
    st.write(output)
    output_dict = json.loads(output)
    st.write(output_dict)
    #question=output_dict["setup"]
    options=output_dict["options"]
    answer=output_dict["answer"]
    st.header("Question")
    st.write(question)
    st.header("Options")
    st.write(options)


#main()
parser2("PHP","Beginner")

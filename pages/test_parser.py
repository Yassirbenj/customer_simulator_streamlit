import streamlit as st
import json
import time

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI

from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field, validator


st.header("test")


def main():
    field=st.text_input("enter an evaluation  field")
    level=st.selectbox("enter level of expertise",options=("Beginner","Intermediate","Expert"))
    start=st.button("start")
    if start:
        result=parser2(field,level)
        if result:
            st.write(result)



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
    model = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=1,openai_api_key=key)

    # Defining data structure.
    class Question(BaseModel):
        setup: str = Field(description="question to evaluate a candidate including a code snippet if exists")
        #additional: str=Field(description="the snippet of the code if the question include a code.")
        options: str=Field(description="possible options for the question asked. the options need to be a numerical list of options. each option should be separated by two semicolons")
        answer: str = Field(description="correct answer to resolve the question. the answer content should be identical to one option ")

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
    query=f"A technical question to evaluate competency of a candidate in field {field} with a level of expertise {level}"
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
    if "properties" in output_dict:
        if isinstance(output_dict["properties"]["setup"], dict):
            question=output_dict["properties"]["setup"]["description"]
        else:
            question=output_dict["properties"]["setup"]
        if isinstance(output_dict["properties"]["options"], dict):
            options=output_dict["properties"]["options"]["description"]
        else:
            options=output_dict["properties"]["options"]
        if isinstance(output_dict["properties"]["answer"], dict):
            answer=output_dict["properties"]["answer"]["description"]
        else:
            answer=output_dict["properties"]["answer"]
    else:
        question=output_dict["setup"]
        options=output_dict["options"]
        answer=output_dict["answer"]
    elements = options.split(";;")
    option_list = [element for element in elements]
    st.header("Question")
    st.write(question)
    st.header("Options")
    response=st.radio("select the best option",option_list,index=None)
    validate=st.button("Validate")
    if validate:
        if response==answer:
            st.write("Correct answer !")
        else:
            st.write("Not the correct answer !")
            st.write(f"The correct answer is: {answer}")

def parser2 (field,level):
    key=st.secrets["openai"]
    model = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=1,openai_api_key=key)

    # Defining data structure.
    class Question(BaseModel):
        setup: str = Field(description="detailed question to evaluate a candidate including a code snippet if exists")
        option1: str=Field(description="first possible option for the question asked.")
        option2: str=Field(description="second possible option for the question asked.")
        option3: str=Field(description="third possible option for the question asked.")
        answer: str = Field(description="correct option to resolve the question. give the option number like option1 or option2. ")

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
    query=f"You're an IT recruiter willing to evaluate a candidate. ask a technical question to evaluate competency of the candidate in field {field} with a level of expertise {level}. Give 3 options of response to choose from. only one option should be correct. each option need to be separated by a comma."
    input_data = {
        "query": query,
        "setup": "Your detailed question here",  # Provide the setup question
        "option1": "First option offered here",
        "option2": "Second option offered here",
        "option3": "third option offered here",# Provide the options for the question
        "answer": "The correct option here from the three options",  # Provide the correct answer
    }

    output = prompt_and_model.invoke(input_data)
    #st.write(output)
    start_json=output.find('{')
    #st.write(start_json)
    output_cleaned=output[start_json-1:]
    st.write(output_cleaned)
    output_dict = json.loads(output_cleaned)
    #st.write(output_dict)
    if "properties" in output_dict:
        if isinstance(output_dict["properties"]["setup"], dict):
            question=output_dict["properties"]["setup"]["description"]
        else:
            question=output_dict["properties"]["setup"]
        if isinstance(output_dict["properties"]["option1"], dict):
            option1=output_dict["properties"]["option1"]["description"]
        else:
            option1=output_dict["properties"]["option1"]
        if isinstance(output_dict["properties"]["option2"], dict):
            option2=output_dict["properties"]["option2"]["description"]
        else:
            option2=output_dict["properties"]["option2"]
        if isinstance(output_dict["properties"]["option3"], dict):
            option3=output_dict["properties"]["option3"]["description"]
        else:
            option3=output_dict["properties"]["option3"]
        if isinstance(output_dict["properties"]["answer"], dict):
            answer=output_dict["properties"]["answer"]["description"]
        else:
            answer=output_dict["properties"]["answer"]
    else:
        question=output_dict["setup"]
        option1=output_dict["option1"]
        option2=output_dict["option2"]
        option3=output_dict["option3"]
        answer=output_dict["answer"]

    st.header("Question")
    st.write(question)
    st.header("Options")

    with st.form(key='quiz_form'):
        response = st.radio("Select the best option", [option1, option2, option3],index=None)
        validate = st.form_submit_button("Validate")

    #response = st.radio("Select the best option", ['option1', 'option2', 'option3'],index=None)
    #validate = st.button("Validate")

        if validate:
            st.write(response)
            st.write(answer)
            if response == answer:
                comparaison="Correct answer !"
                #st.write("Correct answer!")
            else:
                comparaison="Not the correct answer!"
                #st.write(f"The correct answer is: {answer}")
            return response,answer,comparaison

def quizz(question,option1,option2,option3,answer):
    st.header("Question")
    st.write(question)
    st.header("Select the best Options")
    with st.form(key='quiz_form'):
        response = st.radio([option1, option2, option3],index=None)
        validate = st.form_submit_button("Validate")
        if validate:
            if response == answer:
                comparaison="Correct answer !"
            else:
                comparaison="Not the correct answer!"
            st.write(comparaison)

def timer():
    ph = st.empty()
    N = 20
    for secs in range(N,0,-1):
        mm, ss = secs//60, secs%60
        ph.metric("Countdown", f"{mm:02d}:{ss:02d}")
        time.sleep(1)





#main()
#parser2("PHP","Beginner")
quizz('question','a','b','c','c')

from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import os
from dotenv import load_dotenv
import streamlit as st
from streamlit_chat import message
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from typing import List

#openapi_key=os.environ.get("OPENAI_API_KEY")

st.set_page_config(page_title="Customer simulator ")
st.header("Customer simulator")

def main():
    #st.set_page_config(page_title="Customer simulator ")
    #st.header("Customer simulator")
    load_dotenv()

    customer_persona="You are a customer responding to a call from a sales person"
    chat=ChatOpenAI(temperature=0.5)
    with st.sidebar:
        personaes=pd.read_csv('data/personaes.csv',index_col='Personaes')
        personae=st.selectbox('Select your personae',personaes.index, key="personae")
        customer_persona=personaes.iloc[personae,-1]

    if "messages" not in st.session_state:
        st.session_state.messages=[
         SystemMessage(content=customer_persona)
        ]

    if prompt := st.chat_input("Start your call with an introduction"):
      st.session_state.messages.append(HumanMessage(content=prompt))
      with st.spinner ("Thinking..."):
        response=chat(st.session_state.messages)
      st.session_state.messages.append(AIMessage(content=response.content))

    messages=st.session_state.get('messages',[])
    discussion=""

    for i,msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content,is_user=True,key=str(i)+'_saleperson')
            discussion+=f"Sale person: {msg.content}. "
        else:
            message(msg.content,is_user=False,key=str(i)+'_customer')
            discussion+=f"Customer: {msg.content}. "


    evaluate_button=st.button("Evaluate")
    if evaluate_button:
        evaluate(discussion,personae)

    #st.button('Reset Chat', on_click=reset_conversation)

def evaluate(discussion,personae):
    if discussion=="":
        st.write("No discussion to evaluate")
    else:
        llm=OpenAI(temperature=0)

        #context of the discussion
        context= "Evaluate this discussion between a sales person and a customer."
        context+="evaluate if a sales person arguments for a sell are convincing or not."
        context+="please evaluate as regard following factors: "
        context+="Clarity and Relevance,Credibility,Benefits and Value,Objection Handling,Emotional Appeal,Call to Action,Listening Skills,Comparison and Differentiation"
        context+="Please provide a rating over 10 for the sales person per factor and a global rating. Give explanations for each factor. Below the discussion: "

        evaluation = llm(context+discussion)

        st.write(evaluation)

        # store results
        st.cache_data.clear()
        conn = st.experimental_connection("gsheets", type=GSheetsConnection, ttl=1)
        df=conn.read()
        last_index=df.iloc[-1,0]

        #get current time
        current_datetime = datetime.now()

        data={
                "Index":[last_index+1],
                "User":[""],
                "Date":[current_datetime],
                "Personae":[personae],
                "Discussion":[discussion],
                "Evaluation":[evaluation]
            }

        data_df=pd.DataFrame(data)
        data_df_updated=pd.concat([df,data_df])
        conn.update(worksheet="evals",data=data_df_updated)
        st.write("Evaluation stored with success")

        #parser (evaluation)

def evaluate_bis(discussion,personae):
    if discussion=="":
        st.write("No discussion to evaluate")
    else:
        llm=OpenAI(temperature=0)

        #context of the discussion
        context= "You are a sales coach evaluating a discussion between a sales person and a customer."
        context+="evaluate the major point to be improved by the sales person"
        context+="Below the discussion: "

        evaluation = llm(context+discussion)

        st.write(evaluation)



def parser(evaluation):
    class evaluation(BaseModel):
        Clarity: str = Field(description="evaluation rate on clarity")
        Relevance: str = Field(description="evaluation rate on relevance")
        Credibility: str = Field(description="evaluation rate on credibility")
        Benefits: str = Field(description="evaluation rate on benefits")
        Value: str = Field(description="evaluation rate on value")
        Objection_Handling: str = Field(description="evaluation rate on objection handling")
        Emotional_Appeal: str = Field(description="evaluation rate on emotional appeal")
        Call_to_Action: str = Field(description="evaluation rate on call to action")
        Listening_Skills: str = Field(description="evaluation rate on listening skills")
        Comparison: str = Field(description="evaluation rate on comparison")
        Differentiation: str = Field(description="evaluation rate on relevance")

    parser = PydanticOutputParser(pydantic_object=evaluation)

    parsed_eval=parser.parse(evaluation)

    st.write(parsed_eval)


#def reset_conversation():
    #st.write(st.session_state.messages)
    #st.write(st.session_state.messages[0])
    #st.session_state.messages = st.session_state.messages[0]
    #main()


main()

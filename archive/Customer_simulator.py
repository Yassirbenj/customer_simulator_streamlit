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

    personaes=pd.read_csv('data/personaes.csv',index_col='Personaes')
    #st.write(customer_persona)
    personae=st.selectbox('Select your personae',personaes.index, key="personae")
    start=st.button('start')

    if start:
        customer_persona=personaes.iloc[personae-1,-1]
        st.write(customer_persona)

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

        message(messages[0].content,is_user=False,key='_system')

        for i,msg in enumerate(messages[1:]):
            if i % 2 == 0:
                message(msg.content,is_user=True,key=str(i)+'_saleperson')
                discussion+=f"Sale person: {msg.content}. "
            else:
                message(msg.content,is_user=False,key=str(i)+'_customer')
                discussion+=f"Customer: {msg.content}. "


        evaluate_button=st.button("Evaluate")
        if evaluate_button:
            if discussion=="":
                st.write("No discussion to evaluate")
            elif len(messages) <= 5:
                st.write("The discussion is too short to be evaluated")
            else:
                context_coach= "You are a sales coach evaluating a discussion between a sales person and a customer."
                context_coach+="give a feedback to the sales person on the good points and the major point to be improved in his conversation."
                st.session_state.messages=[]
                st.session_state.messages.append(SystemMessage(content=context_coach))
                st.session_state.messages.append(HumanMessage(content=discussion))
                with st.spinner ("Thinking..."):
                    response=chat(st.session_state.messages)
                    good=parser(response.content)[0]
                    improve=parser(response.content)[1]
                st.session_state.messages.append(AIMessage(content=response.content))

                messages_eval=st.session_state.get('messages',[])

                for i,msg in enumerate(messages_eval[2:]):
                    if i % 2 == 0:
                        message(msg.content,is_user=False,key=str(i)+'_coach')

                    else:
                        message(msg.content,is_user=True,key=str(i)+'_candidate')

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
                        "Evaluation":[response.content],
                        "Good":[good],
                        "Improve":[improve]
                    }

                data_df=pd.DataFrame(data)
                data_df_updated=pd.concat([df,data_df])
                conn.update(worksheet="evals",data=data_df_updated)
                st.write("Evaluation stored with success")


    #st.button('Reset Chat', on_click=reset_conversation)




def parser(evaluation):
    st.write(evaluation)
    split_1=evaluation.split(":")
    good=split_1[2]
    split_3=split_1[3].split("Overall,")
    improve=split_3[0]

    return good,improve


#def reset_conversation():
    #st.write(st.session_state.messages)
    #st.write(st.session_state.messages[0])
    #st.session_state.messages = st.session_state.messages[0]
    #main()


main()

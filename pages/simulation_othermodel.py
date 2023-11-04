from langchain.chat_models import ChatCohere
from langchain.llms import OpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.callbacks import get_openai_callback

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

st.set_page_config(page_title="Customer simulator ")
st.header("Customer simulator")

def main():
    cohere_api_key = st.secrets["cohere"]

    chat=ChatCohere(cohere_api_key=cohere_api_key)

    if "messages" not in st.session_state:
        st.cache_data.clear()
        conn_pers = st.experimental_connection("gsheets", type=GSheetsConnection, ttl=1)
        personaes=conn_pers.read(worksheet="personae")
        #st.write(personaes.iloc[:,0])
        #personaes=pd.read_csv('data/personaes.csv',index_col='Personaes')
        #st.write(customer_persona)
        personae=st.selectbox('Select your personae',personaes.iloc[:,0], key="personae")
        start=st.button('Start')
        if start:
            customer_persona=personaes.iloc[personae-1,-2]
            st.session_state.messages=[
                SystemMessage(content=customer_persona)
                ]
            st.session_state.industry=personaes.iloc[personae-1,1]
            st.session_state.position=personaes.iloc[personae-1,2]
            st.session_state.company_size=personaes.iloc[personae-1,3]
            st.session_state.cost=0
        with st.sidebar:
                st.write(personaes.iloc[personae-1,:-2])


    if prompt := st.chat_input("Start your call with an introduction"):
        with st.sidebar:
                st.write(f"Type of contact: Cold call")
                st.write(f"Industry: {st.session_state.industry}")
                st.write(f"Position: {st.session_state.position}")
                st.write(f"Company size: {st.session_state.company_size}")
                st.write(f"Total Cost (USD): {st.session_state.cost}")
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.spinner ("Thinking..."):
                response=chat(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

    messages=st.session_state.get('messages',[])
    discussion=""

    #st.write(messages)

    for i,msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content,is_user=True,key=str(i)+'_saleperson')
            discussion+=f"Sale person: {msg.content}. "
        else:
            message(msg.content,is_user=False,key=str(i)+'_customer')
            discussion+=f"Customer: {msg.content}. "

    if len(messages) > 5:
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
                    with get_openai_callback() as cb:
                        response=chat(st.session_state.messages)
                        st.session_state.cost=round(cb.total_cost,5)
                    #good=parser(response.content)[0]
                    #improve=parser(response.content)[1]
                with st.sidebar:
                    st.write(f"Type of contact: Cold call")
                    st.write(f"Industry: {st.session_state.industry}")
                    st.write(f"Position: {st.session_state.position}")
                    st.write(f"Company size: {st.session_state.company_size}")
                    st.write(f"Total Cost (USD): {st.session_state.cost}")
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
                        #"Personae":[st.session_state.personae],
                        "Discussion":[discussion],
                        "Evaluation":[response.content],
                        #"Good":[good],
                        #"Improve":[improve]
                    }

                data_df=pd.DataFrame(data)
                data_df_updated=pd.concat([df,data_df])
                conn.update(worksheet="evals",data=data_df_updated)
                st.write("Evaluation stored with success")


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

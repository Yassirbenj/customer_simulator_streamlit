from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

import streamlit as st
from streamlit_chat import message
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

st.set_page_config(page_title="Customer simulator ")
st.header("Customer simulator")

def main():
    openai_api_key = st.secrets["openai"]

    chat=ChatOpenAI(model_name='gpt-4',temperature=0.5,openai_api_key=openai_api_key)

    sent_eval=[]

    if "messages" not in st.session_state:
        st.cache_data.clear()
        conn_pers = st.experimental_connection("gsheets", type=GSheetsConnection, ttl=1)
        personaes=conn_pers.read(worksheet="personae")
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
            st.session_state.evals=[]
        with st.sidebar:
                st.write(personaes.iloc[personae-1,:-2])


    if prompt := st.chat_input("Start your call with an introduction"):
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.sidebar:
                st.write(f"Type of contact: Cold call")
                st.write(f"Industry: {st.session_state.industry}")
                st.write(f"Position: {st.session_state.position}")
                st.write(f"Company size: {st.session_state.company_size}")
                st.write(f"Total Cost (USD): {st.session_state.cost}")
                evaluation=evaluate_sentence(prompt)
                st.write(evaluation)
                st.session_state.evals.append({prompt:evaluation})
        with st.spinner ("Thinking..."):
            with get_openai_callback() as cb:
                response=chat(st.session_state.messages)
                st.session_state.cost=round(cb.total_cost,5)
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

    if len(messages) > 5:
        evaluate_button=st.button("Evaluate")
        if evaluate_button:
            if discussion=="":
                st.write("No discussion to evaluate")
            elif len(messages) <= 5:
                st.write("The discussion is too short to be evaluated")
            else:
                recap_response=recap(discussion)
                evaluation_response=evaluate(discussion)
                st.title("Recommendations")
                evaluations=st.session_state.evals
                st.write(evaluations)
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
                        "Evaluation":[evaluation_response],
                        "Recap":[recap_response]
                    }

                data_df=pd.DataFrame(data)
                data_df_updated=pd.concat([df,data_df])
                conn.update(worksheet="evals",data=data_df_updated)
                st.write("Evaluation stored with success")


def recap(discussion):
    openai_api_key = st.secrets["openai"]
    llm=OpenAI(openai_api_key=openai_api_key)
    template = """Question: summarize the discussion between customer and sales person based on following discussion {question} """
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response=llm_chain.run(discussion)
    st.title("Recap of the discussion")
    st.write(response)
    return response

def evaluate_sentence(sentence):
    openai_api_key = st.secrets["openai"]
    llm=OpenAI(openai_api_key=openai_api_key)
    template = """Question: you are a coach for sales persons. this sentence {question} is from a sales person discussing with a customer. do you have a better formulation that will help to improve the sales process?  explain why"""
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response=llm_chain.run(sentence)
    return response

def evaluate(discussion):
    openai_api_key = st.secrets["openai"]
    llm=OpenAI(openai_api_key=openai_api_key)
    template = """Question: you are a coach for sales persons. the last sentence of the following discussion {question} is from a sales person discussing with a customer. do you have a better formulation that will help to improve the sales process?  explain why"""
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response=llm_chain.run(discussion)
    st.title("Evaluation of the discussion")
    st.write(response)
    return response

def config_persona():
    product=st.text_input("What category of product are you selling (ex: CRM, aluminium windows...) ?")
    product_name=st.text_input("whats the name of your product ?")
    #type_customer=st.selectbox("Are you selling to a company or a direct consumer ?",('B2B'))
    industry=st.text_input("To what industry do you want to sell (ex: hotels, construction ) ?")
    department=st.text_input("What department within the company are you calling (ex: finance, operations...) ?")
    reason=st.selectbox("Why are you calling this customer?",('no reason','fulfill a contact form','met in a tradeshow'))
    personnality=st.text_input("what are the main traits of character of your contact person (ex: busy, willing to discuss, impolite...) ?")
    start=st.button("start")
    if start:
        #context
        openai_api_key = st.secrets["openai"]
        llm=OpenAI(openai_api_key=openai_api_key)
        template = """Question: if you are working in department {department} of a company in the industry {industry}, what will be the main points you want to check before buying a product type {product} ?"""
        prompt = PromptTemplate(template=template, input_variables=["department","industry","product"])
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        input_list = {"department": department,"industry": industry,"product": product}
        context=llm_chain(input_list)
        context_text=context["text"]
        #competitors
        llm2=OpenAI(openai_api_key=openai_api_key)
        template2 = """Question: if you are working in a company in the industry {industry}, what will be the main products of type {product} that compete with product {product_name} ?"""
        prompt2 = PromptTemplate(template=template2, input_variables=["industry","product","product_name"])
        llm_chain2 = LLMChain(prompt=prompt2, llm=llm2)
        input_list2 = {"industry": industry,"product": product,"product_name":product_name}
        competition=llm_chain2(input_list2)
        st.write(competition["text"])

config_persona()
#main()

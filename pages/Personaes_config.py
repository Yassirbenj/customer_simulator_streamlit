import streamlit as st
import pandas as pd

uploaded_personaes = st.file_uploader("Upload list of personaes")

if uploaded_personaes is not None:
    df=pd.read_excel(uploaded_personaes,index_col="Personaes")
    st.dataframe(df)

    #prepare the prompt
    df['customer_persona']="You are a responding to a call from a sales person. "
    df['customer_persona']+="You are in the industry of "+ df['Customer industry'] + "."
    df['customer_persona']+=" You have the following position in the company: "+df['Customer position']+"."
    df['customer_persona'] += " The size of your company is " + df['Company size'] +"."
    df['customer_persona'] += " Your Existing technical solutions are: " + df['Technical informations'] +"."
    df['customer_persona'] += " The main pain points in your business are "+ df['Customer pain points'] +"."
    df['customer_persona'] += " your decision making factors are " + df['Decision factors'] +"."
    df['customer_persona'] += " your main personality trait are "+ df['Key personality traits'] +"."
    df['customer_persona'] += " you respond briefly to the question. you are a customer not an assistant "

    df.to_csv('data/personaes.csv',index=True)

import nltk
import streamlit as st
import string
import language_tool_python
import pandas as pd
from collections import Counter


@st.cache
def download():
    nltk.download('punkt')
    nltk.download('stopwords')

download()


def check_grammar(sentence):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(sentence)
    return matches

def grammer_sent(discussion):
    sentences=nltk.sent_tokenize(discussion)
    for sentence in sentences:
        grammar_errors = check_grammar(sentence)
        if grammar_errors:
            st.write(f"In {sentence} found grammar errors: {grammar_errors}")
        else:
            st.write(f"In {sentence} No grammar errors found.")

@st.cache()
def grammer_disc(discussion):
    grammar_errors = check_grammar(discussion)
    return grammar_errors

def tokenize (discussion):
    #remove punctuation
    for punctuation in string.punctuation:
        discussion = discussion.replace(punctuation,'')
    #remove sales person and customer
    discussion=discussion.replace("Sale person",'')
    discussion=discussion.replace("Customer",'')
    st.write(discussion)
    #tokenize
    words=nltk.word_tokenize(discussion)
    st.title("list of words")
    st.write(words)
    st.title("Number of words")
    st.write(len(words))
    counter_object = Counter(words)
    #counter_df=pd.DataFrame.from_dict(counter_object)
    #st.dataframe(counter_df)
    st.write(counter_object)


def json_norm(json_data):
    df0=pd.json_normalize(json_data)
    return df0

discussion=st.text_area("input your paragraph")
if discussion:
    tokenize(discussion)
    st.title("Grammar errors")
    grammar_errors=grammer_disc(discussion)
    if grammar_errors:
        st.write(f"We found {len(grammar_errors)} grammar errors")
        for error in grammar_errors:
            st.write(error)
    else:
        st.write("No grammar errors found.")

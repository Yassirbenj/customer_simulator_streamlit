import nltk
import streamlit as st
import string
import language_tool_python

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

def grammer_disc(discussion):
    grammar_errors = check_grammar(discussion)
    if grammar_errors:
        st.write(f"Found grammar errors: {grammar_errors}")
    else:
        st.write(f"No grammar errors found.")

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
    #grammar errors
    st.title("Grammar errors")

discussion=st.text_area("input your paragraph")
tokenize(discussion)
grammer_disc(discussion)

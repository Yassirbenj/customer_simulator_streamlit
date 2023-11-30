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



discussion=st.text_area("input your paragraph")
if discussion:
    #remove punctuation
    sentences=nltk.sent_tokenize(discussion)
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
    st.title("list&number of sentences")
    st.write(sentences)
    st.write(len(sentences))
    #grammar errors
    st.title("Grammar errors")
    for sentence in sentences:
        grammar_errors = check_grammar(sentence)
        if grammar_errors:
            st.write(f"In {sentence} found grammar errors: {grammar_errors}")
        else:
            st.write(f"In {sentence} No grammar errors found.")

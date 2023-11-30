import nltk
import streamlit as st
import string

nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('english'))


discussion=st.text_area("input your paragraph")
if discussion:
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
    #stop words
    stop_words = [w for w in words if w in stop_words]
    st.title("stop words")
    st.write(stop_words)
    words_cleaned=[w for w in words if not w in stop_words]
    st.title("words without stop words")
    st.write(words_cleaned)
    st.write(len(words_cleaned))

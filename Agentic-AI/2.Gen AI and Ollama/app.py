import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are my investment assistant. Please help me bring me advantage and disadvantage of company I want to invest.You will help me with investment decisions and strategies."),
        ("user", "{question}"),
    ]
)

st.title("Investment Assistant with Gemma 2B")
input_question = st.text_input("Enter your investment question:")

llm = Ollama(model="gemma:2b")
output_parser = StrOutputParser()
chain = prompt| llm | output_parser

if input_question:
    st.write(chain.invoke({'question': input_question}))
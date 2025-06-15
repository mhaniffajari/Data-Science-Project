from fastapi import FastAPI
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
import os
from dotenv import load_dotenv


load_dotenv()
GROQ_API_KEY= os.getenv('GROQ_API_KEY')
model = ChatGroq(model='gemma2-9b-it',api_key=GROQ_API_KEY)
generic_template = "You are {context},Please help me achieve my goal: {goal}"
prompt = ChatPromptTemplate.from_messages(
    [("system",generic_template),("user","{text}")]
)
parser = StrOutputParser()
chain = prompt | model | parser


app = FastAPI(title = 'My Model Assistant',version='0.1.0',description='A simple model assistant using Groq gemma2-9b-it and LangChain')
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost",port=8000)
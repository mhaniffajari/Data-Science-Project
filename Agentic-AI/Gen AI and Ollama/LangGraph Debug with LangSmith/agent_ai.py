from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from typing_extensions import TypedDict
from typing import Annotated
from langchain_core.messages import AIMessage,BaseMessage
from IPython.display import display, Image
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langchain_ollama import ChatOllama
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper,ArxivAPIWrapper
from langchain_community.tools import TavilySearchResults


class State(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]

llm = ChatOllama(model='llama3.1:8b')

def agent_ai_graph():
    graph_workflow = StateGraph(State)

    def call_node(state):
        return {"messages":[llm.invoke(state['messages'])]}
    
    api_wrapper_arxiv = ArxivAPIWrapper(top_k_results=2,doc_content_chars_max=1000)
    arxiv = ArxivQueryRun(api_wrapper=api_wrapper_arxiv)
    api_wrapper_wikipedia = WikipediaAPIWrapper(top_k_results=2,doc_content_chars_max=500)
    wiki = WikipediaQueryRun(api_wrapper=api_wrapper_wikipedia)
    tavily_search_engine = TavilySearchResults(tavily_api_key=tavily_api_key,top_k=2)
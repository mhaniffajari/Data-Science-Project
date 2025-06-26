import os
import warnings
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langserve import add_routes
from mcp_use import MCPAgent, MCPClient
from fastapi_mcp import FastApiMCP

# Suppress resource warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

# Load environment variables
load_dotenv()

# Check if the API key is loaded correctly
google_api_key = os.getenv("GOOGLE_GENAI_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_GENAI_API_KEY is not set in the environment variables.")

# Initialize FastAPI
app = FastAPI(
    title='My Model Assistant',
    version='0.1.0',
    description='A simple model assistant using Gemini 1.5 Flash, LangChain, and LangServe'
)

# Setup MCPAgent and chain
print("Initializing MCPAgent...")
config_file = "weather.json"
client = MCPClient.from_config_file(config_file)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=google_api_key
)

agent = MCPAgent(
    llm=llm,
    client=client,
    max_steps=15,
    memory_enabled=True
)

# Initialize MCP API and mount
mcp = FastApiMCP(app)
mcp.mount()

# Optional: Example if you just want to expose a simple chain
prompt = PromptTemplate.from_template("Answer this question: {question}")
chain = prompt | llm | StrOutputParser()

add_routes(app, chain, path="/agent")

# OR if you want to expose agent's method using RunnableLambda
# Make sure agent has a 'run' method that accepts string input
# agent_runnable = RunnableLambda(lambda x: agent.run(x['input']))
# add_routes(app, agent_runnable, path="/agent")

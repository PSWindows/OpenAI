# Install required libraries
# pip install fastapi langchain openai langchain-community pymssql pyodbc sqlalchemy python-dotenv
#langchain_groq, langchain_core, fastapi, uvicorn, langserve, sse_starlette

from fastapi import FastAPI, HTTPException
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain_groq import ChatGroq
from langchain.sql_database import SQLDatabase
from langchain.prompts.chat import ChatPromptTemplate
from sqlalchemy import create_engine
from langserve import add_routes
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise EnvironmentError("GROQ_API_KEY is not set. Please set it in your environment.")

# Database connection details
# sql - > Host name of the sql server
# sa - > User name  
# OpenAI$$ - > Password
# inventory_db - > Database name
cs = "mssql+pymssql://sa:OpenAI$$@sql/inventory_db"

try:
    db_engine = create_engine(cs)
    db = SQLDatabase(db_engine)
except Exception as e:
    raise ConnectionError(f"Error connecting to the database: {e}")

# Initialize ChatGroq
try:
    llm = ChatGroq(groq_api_key=groq_api_key, model="Gemma2-9b-It")
except Exception as e:
    raise RuntimeError(f"Error initializing LLM: {e}")

# Define SQL toolkit and agent
sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system",
         """
         You are a very intelligent AI assistant who is an expert in identifying relevant questions from users and converting them into SQL queries to generate correct answers.
         Use the following context to write Microsoft SQL queries, do not use MySQL queries.
         Context:
         Query against the connected database, which has two tables: tbl_inv and tbl_os.
         tbl_os has tbl_OS_ID, OSName. It gives OS information.
         tbl_inv has ServerName, IP, Location, ApplicationRunning, Owner, tbl_inventory_OS_ID. It gives server information.
         Use joins whenever required.
         """
         ),
        ("user", "{text}")
    ]
)

agent = create_sql_agent(
    llm=llm,
    toolkit=sql_toolkit,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_execution_time=100,
    max_iterations=1000
)

# Create FastAPI app
app = FastAPI(
    title="Langchain API Server",
    version="1.0",
    description="A simple API server using Langchain runnable interfaces"
)

# Add routes for the chain
add_routes(app, agent, path="/chain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8005)

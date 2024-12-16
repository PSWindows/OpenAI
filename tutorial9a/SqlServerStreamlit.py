# Install required libraries
# pip install streamlit langchain openai langchain-community pymssql pyodbc sqlalchemy python-dotenv

import streamlit as st
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain.prompts.chat import ChatPromptTemplate
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY is not set. Please set it in your environment.")
    st.stop()


# Streamlit app setup
st.set_page_config(page_title="AI App to Chat with SQL DB")
st.header("Ask Anything About Your Database")

query = st.text_input("Ask your question here:")

# Database connection details
cs = "mssql+pymssql://sa:OpenAI$$@localhost/inventory_db"
try:
    db_engine = create_engine(cs)
    db = SQLDatabase(db_engine)
except Exception as e:
    st.error(f"Error connecting to the database: {e}")
    st.stop()

# Initialize ChatOpenAI
try:
    llm = ChatOpenAI(openai_api_key=api_key, temperature=0.0, model="gpt-3.5-turbo")
except Exception as e:
    st.error(f"Error initializing LLM: {e}")
    st.stop()

# Define SQL toolkit and agent
sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
        """
        you are a very intelligent AI assistant who is expert in identifing relevant questions from user and converting into sql queriers to generate coorect answer.
        Please use the belolw context to write the microsoft sql queries, dont use mysql queries.
        context:
        you must query against the connected database,it has total 2 tables,they are tbl_inv,tbl_os.
        tbl_os has tbl_OS_ID, OSName. it gives OS information
        tbl_inv has ServerName, IP, Location, ApplicationRunning, Owner, tbl_inventory_OS_ID. it gives server information
        As an expert you must use joins whenewver required.
        """
        ),
        ("user", "{question}")
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

# Handle the query submission
if st.button("Submit", type="primary"):
    if query:
        try:
            
            formatted_prompt = prompt.format(question=query)
            response = agent.run(formatted_prompt)
            st.write(response)
        except Exception as e:
            st.error(f"Error processing the query: {e}")

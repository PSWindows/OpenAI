#pip install sqlalchemy llama-index


from sqlalchemy import (
    create_engine,
    text, 
)
from llama_index.core import SQLDatabase
from llama_index.llms.openai import OpenAI
from sqlalchemy import create_engine

db_user = "root"
db_password = "OpenAI"
db_host = "localhost:3306"
db_name = "db_inventory"
connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_engine(connection_string)

print("Printing three rows:")
with engine.connect() as connection:
    result = connection.execute(text("select * from tbl_os limit 3"))
    for row in result:
        print(row)
        
print("Printing Table structure:")
with engine.connect() as connection:
    result = connection.execute(text("describe tbl_os"))
    for row in result:
        print(row)   

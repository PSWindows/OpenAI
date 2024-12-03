"""
If we don't know ahead of time which table we would like to use, and the total size of the table schema overflows your context window size, 
we should store the table schema in an index so that during query time we can retrieve the right schema.
The way we can do this is using the SQLTableNodeMapping object, which takes in a SQLDatabase and produces a Node object 
for each SQLTableSchema object passed into the ObjectIndex constructor.

If you don't know which table you'll query or if the schema is too large for the model's context, you can use SQLTableNodeMapping to convert 
each table schema into "Node" objects. These nodes are stored in an ObjectIndex. At query time, the index retrieves only the relevant schema, 
optimizing memory usage and ensuring efficient, dynamic query execution.
"""
#pip install sqlalchemy llama-index
#pip install pymysql

import os
from dotenv import load_dotenv
from llama_index.core import SQLDatabase
from llama_index.llms.openai import OpenAI
from sqlalchemy import create_engine
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex

db_user = "root"
db_password = "OpenAI"
db_host = "localhost:3306"
db_name = "db_inventory"
connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
engine = create_engine(connection_string)


# here we define our SQLDatabase abstraction (a light wrapper around SQLAlchemy)
sql_database = SQLDatabase(engine, include_tables=["tbl_inventory", "tbl_os"])

from sqlalchemy import (
    create_engine,
    text, 
)

from llama_index.core.indices.struct_store.sql_query import (
    SQLTableRetrieverQueryEngine,
)
from llama_index.core.objects import (
    SQLTableNodeMapping,
    ObjectIndex,
    SQLTableSchema,
)


table_node_mapping = SQLTableNodeMapping(sql_database)
table_schema_objs = [
    SQLTableSchema(table_name="tbl_inventory"),
    SQLTableSchema(table_name="tbl_os")

]  # add a SQLTableSchema for our table, you may add more tables here

# The ObjectIndex class allows for the indexing of arbitrary Python objects including SQL database schema objects. 
obj_index = ObjectIndex.from_objects(
    table_schema_objs, 
    table_node_mapping,
   index_cls=VectorStoreIndex,)
query_engine = SQLTableRetrieverQueryEngine(
    sql_database, obj_index.as_retriever(similarity_top_k=3)
)

query_str = "give me all the server inventory including os in CSV format."
#query_str = "Bob manages what server and give all the details in CSV format"
response = query_engine.query(query_str)

print(response)

# pip install flask
from flask import Flask, render_template, request, jsonify
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
from llama_index.core.query_engine import RetrieverQueryEngine
import os

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Set up the OpenAI LLM
llm = OpenAI(model="gpt-3.5-turbo")

# Load data using SimpleDirectoryReader
documents = SimpleDirectoryReader("data").load_data()

# Create the index from the documents
index = VectorStoreIndex.from_documents(documents)

# Set up the retriever
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10,  # Retrieve the top 10 most similar documents
)

# Create the query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
)

# Initialize Flask app
app = Flask(__name__)

# Route for the chatbot interface
@app.route("/")
def home():
    return render_template("index.html")

# API endpoint for processing queries
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data.get("question")
    if not user_input:
        return jsonify({"error": "Invalid input"}), 400

    Myquery = f"User: {user_input}\nAI:"
    AIresponse = query_engine.query(Myquery)
    return jsonify({"response": AIresponse.response})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

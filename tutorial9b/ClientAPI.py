import requests
import streamlit as st
import json


def get_groq_response(input_text):
    # Construct the JSON body with the user input

    json_body = {
        "input": {
            "input": input_text
        },
        "config": {},
        "kwargs": {}
    }
      

   # Send POST request to the FastAPI server
    response = requests.post(
        "http://127.0.0.1:8005/chain/invoke",  # Endpoint for the chain invocation
        headers={"Content-Type": "application/json"},  # Specify JSON content type
        data=json.dumps(json_body)  # Convert the Python dictionary to a JSON string
    )

    # Check for errors in the response
    if response.status_code == 200:
        result = response.json().get("output", {}).get("output", "No output found in the response")  # Return the JSON response from the server
        return result
    else:
        return {"error": f"Failed with status code {response.status_code}", "details": response.text}

# Streamlit app
st.title("LLM Application Using LCEL")

# Input field for user text
input_text = st.text_input("Search for the servers")

# Process the input and display the response
if input_text:
    response = get_groq_response(input_text)  # Get the response from FastAPI
    st.write(response)  # Display the response in the Streamlit app
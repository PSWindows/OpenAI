import requests
import base64
import os
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from dotenv import load_dotenv
load_dotenv()
PASSWORD  = os.getenv("PASSWORD_SNOW")

# Combined function to fetch incidents by year or date range
def get_incidents(instance: str, username: str, password: str, year: int = None, start_date: str = None, end_date: str = None) -> list:
    """
    Fetch incidents from ServiceNow for a specific year or date range.

    Parameters:
        - instance (str): ServiceNow instance name.
        - username (str): ServiceNow username.
        - password (str): ServiceNow password.
        - year (int, optional): Year to fetch incidents for.
        - start_date (str, optional): Start date in YYYY-MM-DD format.
        - end_date (str, optional): End date in YYYY-MM-DD format.

    Returns:
        - list: A list of incidents with selected fields or an error message.
    """
    if year:
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
    elif not (start_date and end_date):
        return {"error": "Either year or both start_date and end_date must be provided."}

    # Build the URL
    url = f"https://{instance}.service-now.com/api/now/table/incident?sysparm_query=opened_at>={start_date}^opened_at<={end_date}&sysparm_limit=50"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic " + base64.b64encode((username + ":" + password).encode()).decode(),
    }

    # API request
    response = requests.get(url, headers=headers)

    # Parse response
    if response.status_code == 200:
        return [
            {
                "number": incident["number"],
                "short_description": incident.get("short_description", ""),
                "opened_at": incident["opened_at"],
            }
            for incident in response.json().get("result", [])
        ]
    else:
        return {"error": response.text}


# Define the FunctionTool
find_incidents_tool = FunctionTool.from_defaults(
    fn=lambda year=None, start_date=None, end_date=None: get_incidents(
        instance="dev290401",
        username="admin",
        password=PASSWORD,
        year=year,
        start_date=start_date,
        end_date=end_date
    ),
    name="find_incidents",
    description="Fetches incidents for a given year or date range from ServiceNow. Parameters: year (int), start_date (str), end_date (str)."
)

# List of tools
tools = [find_incidents_tool]

# LLM setup
llm = OpenAI(model="gpt-3.5-turbo")

# Agent setup
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, max_iterations=1000)

# Example Queries
#response = agent.chat("Find all incidents from the year 2018. Provide results in CSV format.")
#response= agent.chat("Give me the incident INC0009009 details")
response = agent.chat("Find all incidents from 2018/08/30 to 2018/08/31. Provide results in CSV format.")

# Print responses

print(response)
#print("\nResponse for date range 2018-08-30 to 2018-08-31:")
#print(response_date_range)

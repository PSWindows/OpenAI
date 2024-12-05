import requests
import os
from dotenv import load_dotenv
# Define ServiceNow credentials and instance details

load_dotenv()


USERNAME = "admin"
PASSWORD= os.getenv("PASSWORD")
print(PASSWORD)

INSTANCE = "dev290401"
BASE_URL = f"https://{INSTANCE}.service-now.com/api/now/table"

# Helper function to make GET requests
def make_get_request(api_url):
    auth = (USERNAME, PASSWORD)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = requests.get(api_url, auth=auth, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from {api_url}. Status Code: {response.status_code}")
        return None

# Function to fetch incidents from ServiceNow
def fetch_incidents():
    api_url = f"{BASE_URL}/incident"
    response = make_get_request(api_url)
    if response:
        return response.get('result', [])
    return []

# Function to fetch user details from the sys_user table
def fetch_user_details(caller_id):
    api_url = f"{BASE_URL}/sys_user/{caller_id}"
    response = make_get_request(api_url)
    if response:
        user_info = response.get('result', {})
        return f"{user_info.get('first_name', 'N/A')} {user_info.get('last_name', 'N/A')}"
    return 'N/A'

# Entry point for the script
def handle_Main():
    print("Welcome Type 'exit' to quit.")
    while True:
        user_input = input("Enter see all incidents or type the incident number to see specific incident: ")
        if user_input.lower() == "exit" or user_input.lower() == "quit" :
            print("Goodbye!")
            break
        
        # Check if the user is asking for specific incident details
        #if "incident" in user_input.lower():
        if user_input and user_input.strip():
            incident_number=user_input
            incidents_documents = fetch_incidents()
            incident_info_list = [doc for doc in incidents_documents if incident_number in doc.get('number', '')]
        else:
            incident_info_list = [doc for doc in incidents_documents]
        

        if incident_info_list:
            print(f"Here str the information for Incident:\n")
            for incident_info in incident_info_list:
                # Extract incident details
                short_description = incident_info.get('short_description', 'N/A')
                state = incident_info.get('state', 'N/A')
                urgency = incident_info.get('urgency', 'N/A')
                opened_at = incident_info.get('opened_at', 'N/A')
                caller_id = incident_info.get('caller_id', {}).get('value', 'N/A')
                number = incident_info.get('number', 'N/A')
                
                # Fetch caller details
                caller = fetch_user_details(caller_id)

                # Print the details

                print(f"Incident Number: {number}")
                print(f"Short Description: {short_description}")
                print(f"State: {state}")
                print(f"Urgency: {urgency}")
                print(f"Opened: {opened_at}")
                print(f"Caller: {caller}")
                print("--------------------------------")
        else:
            print(f"Bot: Incident not found.")

# Entry point for the script
if __name__ == "__main__":
    handle_Main()

import requests
import json
import os
"""
def send_post_request(message):
    # Retrieve environment variables
    base_url = os.getenv("GOVBOTIC_API_BASE_URL", "http://127.0.0.1:8000")
    token = os.getenv("GOVBOTIC_API_TOKEN", "FAKE TOKEN")
    
    # Construct the URL using the base_url environment variable
    url = f"{base_url}/message/"
    
    # Include the token in the headers
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    data = {
        "requestType": "query",
        "persona": "examplePersona",
        "userID": "exampleUID",
        "message": message,  # Use the message parameter here
        "document": "This is an example document text.",
        "context": "Asking about weather conditions in New York City.",
        "maxTokens": 100,
        "temperature": 0.5,
        "sessionId": "exampleUID",
        "language": "en-US",
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()  # Return the response as a JSON object
"""
import requests
import json
import os

def send_post_request(endpoint,message):
    # Retrieve environment variables
    base_url = os.getenv("GOVBOTIC_API_BASE_URL", "http://127.0.0.1:8000")
    token = os.getenv("GOVBOTIC_API_TOKEN", "FAKE TOKEN")

    # Construct the URL using the base_url environment variable
    url = f"{base_url}/{endpoint}/"

    # Include the token in the headers
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    # Ensure the data dictionary matches the ConversationRequest structure
    data = {
        "requestType": "query",
        "persona": "examplePersona",
        "uid": "exampleUID",  # Corrected from userID to uid
        "message": message,  # Use the message parameter here
        "document": "This is an example document text.",
        "context": "Asking about weather conditions in New York City.",
        "maxTokens": 100,
        "temperature": 0.5,
        "sessionId": "exampleSessionId",  # Updated to match the previous sessionId discussion
        "language": "en-US",
    }

    # Perform the POST request
    response = requests.post(url, headers=headers, json=data)  # Using json=data automatically sets Content-Type and serializes the data
    print("-------------->",response)
    return response.json()  # Return the response as a JSON object


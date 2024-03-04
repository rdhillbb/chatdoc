import requests
import json

# Assuming GOVBOTIC_API_BASE_URL is the environment variable for your API's base URL
GOVBOTIC_API_BASE_URL = "http://localhost:8000"  # Replace with the actual base URL
endpoint = "/setfiledrawer/"
url = f"{GOVBOTIC_API_BASE_URL}{endpoint}"

# Construct a request payload matching the ConversationRequest model
request_payload = {
    "requestType": "setchatfile",
    "persona": "AI Assistant",
    "uid": "user123",  # Note: 'userId' field is aliased to 'uid' in the JSON payload
    "message": "/CHAINOFTHOUGHT/2201.11903",
    "document": None,
    "context": "User asks for help.",
    "maxTokens": 150,
    "temperature": 0.5,
    "sessionId": "session456",
    "language": "en"
}

# Replace 'your_bearer_token_here' with your actual bearer token
bearer_token = "your_bearer_token_here"

# Headers including Content-Type and Authorization with the bearer token
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {bearer_token}"
}

# Send the POST request
response = requests.post(url, headers=headers, data=json.dumps(request_payload))

# Check if the request was successful
if response.status_code == 200:
    # Parse the response to JSON
    response_json = response.json()
    
    # Assuming successful request, print the response content
    print("Response received from server:")
    print(json.dumps(response_json, indent=4))
else:
    print(f"Failed to get a successful response, status code: {response.status_code}")
    print("Response:", response.text)


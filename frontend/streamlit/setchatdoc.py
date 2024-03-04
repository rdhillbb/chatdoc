import requests
import json

def setchatDoc(doc: str):
    # Assuming GOVBOTIC_API_BASE_URL is the environment variable for your API's base URL
    GOVBOTIC_API_BASE_URL = "http://localhost:8000"  # Replace with the actual base URL
    endpoint = "/setfiledrawer/"
    url = f"{GOVBOTIC_API_BASE_URL}{endpoint}"

    # Construct a request payload matching the ConversationRequest model
    request_payload = {
        "requestType": "setchatfile",
        "persona": "system",
        "uid": "user123",
        "message": doc,  # Setting message to the passed 'doc' parameter
        "document": None,
        "context": "User asks for help.",
        "maxTokens": 0,
        "temperature": 0,
        "sessionId": "nosession",
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
        print("Response received from server:")
        print(json.dumps(response_json, indent=4))
    else:
        print(f"Failed to get a successful response, status code: {response.status_code}")
        print("Response:", response.text)
"""
def main():
    # Call setchatDoc with the specific document reference
    setchatDoc("/CHAINOFTHOUGHT/2201.11903")

if __name__ == "__main__":
    main()
"""

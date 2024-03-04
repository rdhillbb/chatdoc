import requests
import json
import os

def send_post_request():
    # Retrieve the base URL from the environment variable
    base_url = os.getenv('GOVBOTIC_API_BASE_URL', 'http://127.0.0.1:8000')  # Default to localhost if not set
    url = f'{base_url}/message/'
    
    # Replace 'YourTokenHere' with your actual Bearer token value
    bearer_token = 'YourTokenHere'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {bearer_token}'  # Authorization header with Bearer token
    }
    
    data = {
        "persona": "examplePersona",
        "uid": "exampleUID",
        "message": "What are the health Benefits of Lemmon Peels",
        "document": "LemonPeel/LemmonPeels",
        "context": "Asking about weather conditions in New York City.",
        "maxTokens": 100,
        "temperature": 0.5,
        "topP": 0.9,
        "stopSequences": ["\n"],
        "sessionId": "exampleUID",
        "language": "en-US",
        "requestType": "query"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response

if __name__ == "__main__":
    response = send_post_request()
    if response.status_code == 200:
        print("Success:")
        print(response.json())
    else:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)


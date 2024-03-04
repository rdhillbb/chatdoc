import requests
import json
import os


def send_post_request(endpoint, message, document):
    # Retrieve environment variables
    base_url = os.getenv("GOVBOTIC_API_BASE_URL", "http://127.0.0.1:8000")
    token = os.getenv("GOVBOTIC_API_TOKEN")

    # Construct the URL using the base_url environment variable
    url = f"{base_url}/{endpoint}/"

    # Include the token in the headers
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    # Updated data dictionary to match the cURL script
    data = {
        "persona": "examplePersona",
        "uid": "exampleUID",
        "message": message,
        "document": document,
        "context": "What is the Purpose of this manual?",
        "maxTokens": 100,
        "temperature": 0.5,
        "topP": 0.9,
        "stopSequences": ["\n"],
        "sessionId": "exampleUID",  # Ensure this matches 'uid' if necessary
        "language": "en-US",
        "requestType": "query"
    }

    # Perform the POST request with error handling
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        return response.json()  # Return the response as a JSON object
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")
"""
# Example usage
if __name__ == "__main__":
    response = send_post_request("message", "Health Benefits of Lemons", "LemonPeel/LemmonPeels")
    print(response)
"""

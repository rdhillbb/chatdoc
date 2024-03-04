import requests
import os

def upload_file(filedrawer, file_url):
    # Retrieve the server URL from an environment variable
    server_url = os.getenv('GOVBOTIC_ADMIN_SERVER', 'http://localhost:8050')
    
    # Append the specific endpoint to the server URL
    url = f'{server_url}/ingestlocalweb/'
    
    data = {
        "request": "upload",
        "filedrawer": filedrawer,
        "filename": file_url
    }

    response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
    
    # Check if the request was successful
    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Error:", response.status_code, response.text)

# Example usage
filedrawer = "RGarlic"
file_url = "https://www.webmd.com/vitamins/ai/ingredientmono-300/garlic"
upload_file(filedrawer, file_url)


import sys
import json
import os
from typing import List, Optional
from pydantic import BaseModel, Field
import requests
sys.path.append('../..')
from objmsg.messagedef import FileOperationReq,FileOperationResp,ErrorResponse

# Assuming environment variables are set for API base URL and token
GOVBOTIC_API_BASE_URL = os.getenv("GOVBOTIC_API_BASE_URL")
GOVBOTIC_API_TOKEN = os.getenv("GOVBOTIC_API_TOKEN")

# Prepare the request data
request_data = FileOperationReq(
    requestType="listfiles",
    dataOperands="YourDataOperands",
    fileNames=["file1.txt", "file2.txt"]  # This is optional
)

# Prepare headers with the Bearer token
headers = {
    "Authorization": f"Bearer {GOVBOTIC_API_TOKEN}",
    "Content-Type": "application/json"
}

# Perform the HTTP request
response = requests.post(
    f"{GOVBOTIC_API_BASE_URL}/listfiledrawers/",
    headers=headers,
    json=request_data.dict()  # Convert Pydantic model to dict for JSON serialization
)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response using FileOperationResp model for validation and convenience
    response_data = FileOperationResp.parse_obj(response.json())
    print(json.dumps(response.json(), sort_keys=True, indent=4))
    print()
    print()
    print("Response received successfully:", response_data)
else:
    print("Failed to receive a valid response:", response.text)


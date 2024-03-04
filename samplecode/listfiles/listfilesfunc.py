import os,sys
import requests
from typing import List, Optional
from pydantic import BaseModel, Field

sys.path.append('../..')
from objmsg.messagedef import FileOperationReq,FileOperationResp,ErrorResponse

# Function to list documents
def listdocs() -> List[str]:
    GOVBOTIC_API_BASE_URL = os.getenv("GOVBOTIC_API_BASE_URL")
    GOVBOTIC_API_TOKEN = os.getenv("GOVBOTIC_API_TOKEN")

    request_data = FileOperationReq(
        requestType="listfiles",
        dataOperands="YourDataOperands"
        # fileNames field is optional for listing, so it's omitted here
    )

    headers = {
        "Authorization": f"Bearer {GOVBOTIC_API_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"{GOVBOTIC_API_BASE_URL}/listfiledrawers/",
        headers=headers,
        json=request_data.dict()  # Convert Pydantic model to dict for JSON serialization
    )

    if response.status_code == 200:
        response_data = FileOperationResp.parse_obj(response.json())
        if response_data.responseMsg:
            return response_data.responseMsg  # Return the list of file names
        else:
            return ["No files found or responseMsg is empty."]
    else:
        print("Failed to receive a valid response:", response.text)
        return ["Failed to retrieve file list due to an error."]  # Return an error message as a list

# Example usage of the listdocs function
if __name__ == "__main__":
    file_list = listdocs()
    print("List of documents:", file_list)


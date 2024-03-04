import sys
from fastapi import FastAPI, HTTPException, Header, Depends
import os
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

sys.path.append("../")
from fileops.fileutl import list_dir
from chains.fchains import createLchain, createDchain, createQchain
from objmsg.genloader import GMyLoader
from fileops.onlinedownload import is_valid_download_url
from objmsg.messagedef import (
    ConversationRequest,
    ConversationResponse,
    ErrorResponse,
    FileOperationResp,
    FileOperationReq,
)

# Your existing Pydantic models
# Initialize your rag_chain or equivalent processing logic
rag_chain = ""
errjson = """
{
}"""


def is_valid_file_path(file_path):
    return os.path.isfile(file_path)


def ptime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time:", current_time)


def is_valid_directory(path):
    # Check if the path exists and is a directory
    if os.path.exists(path) and os.path.isdir(path):
        print(f"The path '{path}' is a valid directory.")
        return True
    else:
        print(f"The path '{path}' is not a valid directory.")
        return False


# Example usage


# Usage example
app = FastAPI()


# Dependency for extracting the bearer token
async def get_token(authorization: Optional[str] = Header(None)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        return token
    else:
        raise HTTPException(status_code=401, detail="Unauthorized or missing token.")


from fastapi import FastAPI, HTTPException, Depends

# Import Pydantic models (assumed to be defined elsewhere in your code)

app = FastAPI()


@app.post("/message/", response_model=ConversationResponse)
async def receive_message(
    message_request: ConversationRequest, token: str = Depends(get_token)
):
    # Token is now accessible within this function
    print(f"Received token: {token}")

    try:
        # Example processing logic based on the requestType
        print()
        print("----------")
        ptime()
        print("operation: ", message_request.requestType)
        if message_request.requestType == "query":
            # Check if rag_chain is initialized (assuming it's a global or external dependency)
            # if not rag_chain:
            if 1 < 0:
                content = "Server Offline"
            else:
                if message_request.document == "":
                    raise Exception("No file drawer and document specified.")
                rag_chain = createLchain(message_request.document)
                content = rag_chain.invoke(message_request.message)

            input_token_count = len(
                message_request.message.split()
            )  # Simplified example
            output_token_count = len(content.split())  # Simplified example
            citations = [
                "source=document.txt,page=1,date=01/22/2024"
            ]  # Example citation

            # Constructing and returning the ConversationResponse object
            return ConversationResponse(
                requestType=message_request.requestType,
                content=content,
                citations=citations,
                inputTokenCount=input_token_count,
                outputTokenCount=output_token_count,
                error=None,  # Assuming no error, otherwise populate this field accordingly
            )
        else:
            # For unsupported request types, consider raising an exception to use FastAPI's error handling
            raise HTTPException(status_code=400, detail="Unsupported request type.")

    except Exception as e:
        # Handle unexpected errors
        print(f"An error occurred: {str(e)}")
        errmsg = f"An error occurred: {str(e)}"
        errms = ErrorResponse(code="99", message=errmsg)
        # Return a generic error response or customize based on the exception if needed
        return ConversationResponse(
            requestType="ERROR",
            content=errmsg,
            citations=["ERROR"],
            inputTokenCount=0,
            outputTokenCount=0,
            error=None,
        )


@app.post("/setfiledrawer/", response_model=ConversationResponse)
async def receive_message(
    message_request: ConversationRequest, token: str = Depends(get_token)
):
    global rag_chain
    # Token is now accessible within this function
    print(f"Received token: {token}")
    print()
    print("----------")
    ptime()
    print("operation: ", message_request.requestType)
    try:
        # Example processing logic based on the requestType
        if message_request.requestType == "setchatfile":
            print("Setting File Drawer", message_request.message)
            rag_chain = createLchain(message_request.message)
            # Example token counts and citations (these should be calculated/defined based on actual logic)
            input_token_count = 0  # Simplified example
            output_token_count = 0  # Simplified example
            citations = [""]  # Example citation

            # Constructing and returning the MessageResponse object
            return ConversationResponse(
                requestType=message_request.requestType,
                content="Current Chat File:" + message_request.message,
                citations=citations,
                inputTokenCount=input_token_count,
                outputTokenCount=output_token_count,
                error=None,  # Assuming no error, otherwise populate this field accordingly
            )
        else:
            # Handling unsupported request types explicitly raises an exception
            raise HTTPException(status_code=400, detail="Unsupported request type.")
    except Exception as e:
        # Handle unexpected errors
        print(f"An error occurred: {str(e)}")
        errmsg = f"An error occurred: {str(e)}"
        # Return a generic error response or customize based on the exception if needed
        return ConversationResponse(
            requestType=message_request.requestType,
            content=None,
            citations=[],
            inputTokenCount=0,
            outputTokenCount=0,
            error={"code": "99", "message": errmsg},
        )


@app.post("/listfiledrawers/", response_model=FileOperationResp)
async def receive_message(
    message_request: FileOperationReq, token: str = Depends(get_token)
):
    try:
        # Token is now accessible within this function

        print(f"Received token: {token}")
        print()
        print("----------")
        ptime()
        print("operation: ", message_request.requestType)
        # Example processing logic based on the requestType
        if message_request.requestType == "listfiles":
            topdir = os.environ.get("GOVBOTIC_INGESTION_STORAGE")
            filelist = list_dir(topdir)
            # Constructing and returning the MessageResponse object
            return FileOperationResp(
                responseType="OK",
                responseMsg=filelist,
                error=None,  # Assuming no error, otherwise populate this field accordingly
            )
        else:
            # Handling unsupported request types
            return FileOperationResp(
                responseType="Error",
                responseMsg=errjson,
                error=ErrorResponse(
                    code="01",
                    message="Invalid Request Type: " + message_request.requestType,
                ),  # Assuming no error, otherwise populate this field accordingly
            )

    except Exception as e:
        # Here, you handle any unexpected errors that occur during processing
        # You may want to log the error or take other actions depending on your application's requirements
        print(f"An error occurred: {str(e)}")
        errmsg = f"An error occurred: {str(e)}"
        # Return a generic error response or customize based on the exception if needed
        return FileOperationResp(
            responseType="Error",
            responseMsg=errmsg,
            error=None,
        )

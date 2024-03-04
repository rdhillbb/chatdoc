from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import sys 
from pathlib import Path
from typing import List
import os
from pydantic import BaseModel, Field
sys.path.append("../")
from ingestfiles import setupingest,ing_singlefile
from objmsg.messagedef import ErrorResponse,ResponseFileUpload
from fileops.onlinedownload import is_valid_download_url
from fileops.webfildload import download_file
from datetime import datetime
from objmsg.messagedef import ErrorResponse, REQLocalWebFile, RESPLocalWebFile
from util.ftime import distime
# Define your Pydantic models here


app = FastAPI()

def list_files_with_paths(directory):
    path = Path(directory)
    return [str(file) for file in path.glob("*") if file.is_file()]


@app.post("/uploadfile/", response_model=ResponseFileUpload)
async def upload_file(filedrawer: str = Form(...), files: List[UploadFile] = File(...)):
    base_temp_dir = os.environ["GOVBOTIC_INGESTION_STORAGE"]  # Adjust as necessary
    target_dir = os.path.join(base_temp_dir, filedrawer,)
    os.makedirs(target_dir, exist_ok=True)

    uploaded_files = []
    filelist = []
    print("UPLOADIN")
    distime()
    try:
        for file in files:
            filename, fileext = os.path.splitext(file.filename)
            targetdir = os.path.join(target_dir,filename,)
            os.makedirs(targetdir, exist_ok=True)
            file_location = os.path.join(targetdir,file.filename)
            print(file_location)
            with open(file_location, "wb+") as file_object:
                content = await file.read()  # Read file content
                file_object.write(content)  # Write to the target file
                #uploaded_files.append(file.filename)
                uploaded_files.append(file_location)
                print(file_location)
                  # Add filename to the list
        filelist = list_files_with_paths(target_dir)
        for file_path in uploaded_files:
             print(file_path)
             #ingfile = setupingest(target_dir, file_path)
             msg = ing_singlefile(file_path)
             print(file_path)
        return ResponseFileUpload(
            message=f"Successfully uploaded {len(files)} files to '{filedrawer}'.",
            listfiles=uploaded_files,
        )
    except Exception as e:
        return ResponseFileUpload(
            message="Failed to upload files.",
            error=ErrorResponse(code="FileUploadError", message=str(e)),
        )


# Define the POST endpoint
@app.post("/ingestlocalweb/", response_model=RESPLocalWebFile)
async def upload_file(request_data: REQLocalWebFile):
    # Log request
    print("REQUEST")
    distime()
    request_data.pretty_print()
    try:
        dloadedfile = None  # Initialize to None

        # Check if the URL is valid for downloading
        if is_valid_download_url(request_data.filename):
            dloadedfile = download_file(request_data.filename)
            ingfile = setupingest(request_data.filedrawer, dloadedfile)
            msg = ing_singlefile(ingfile)
            print(msg)
            response = RESPLocalWebFile(
                request=request_data.request, status="success", error=None
            )
        elif os.path.exists(request_data.filename):
            # Assuming you might need to download the file if it doesn't exist locally
            ingfile = setupingest(request_data.filedrawer, request_data.filename)
            msg = ing_singlefile(ingfile)
            print(msg)
            response = RESPLocalWebFile(
                request=request_data.request, status="success", error=None
            )
        else:
            # Handle case where file does not exist and is not a valid download URL
            raise ValueError("The file does not exist or URL is invalid.")
    except Exception as e:
        print(f"Error processing request: {e}")
        # Construct an error response
        response = RESPLocalWebFile(
            request=request_data.request, 
            status="failure",
            error=ErrorResponse(code="ErrorProcessingRequest", message=str(e))
        )
    print("<><><><><><>")
    return response


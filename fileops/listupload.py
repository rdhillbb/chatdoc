import os
import requests
from typing import List

def upload_file_to_endpoint(filepath: str, filedrawer: str, url: str) -> str:
    """
    Upload a file to a REST endpoint.
    
    :param filepath: Path to the file to upload.
    :param filedrawer: Target directory (or drawer) for the uploaded file.
    :param url: URL of the REST endpoint.
    :return: A message indicating the outcome of the upload.
    """
    files = {'files': (os.path.basename(filepath), open(filepath, 'rb'))}
    data = {'filedrawer': filedrawer}
    response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        return f"Successfully uploaded {os.path.basename(filepath)} to {filedrawer}."
    else:
        return f"Failed to upload {os.path.basename(filepath)}. Status code: {response.status_code}"

def upload_files_from_source(filedrawer: str, sourcedir: str, url: str) -> List[str]:
    """
    Upload a file or all files from a directory to a REST endpoint.
    
    :param filedrawer: The target drawer where files will be uploaded.
    :param sourcedir: Path to the source file or directory.
    :param url: URL of the REST endpoint.
    :return: A list of messages indicating the outcome of each upload.
    """
    if os.path.isfile(sourcedir):
        # If sourcedir is a file, upload it
        return [upload_file_to_endpoint(sourcedir, filedrawer, url)]
    elif os.path.isdir(sourcedir):
        # If sourcedir is a directory, upload all files in it
        messages = []
        for filename in os.listdir(sourcedir):
            filepath = os.path.join(sourcedir, filename)
            if os.path.isfile(filepath):
                messages.append(upload_file_to_endpoint(filepath, filedrawer, url))
        return messages
    else:
        return ["The sourcedir provided does not exist as a file or directory."]

# Example usage
"""
filedrawer = "Raindow"
sourcedir = "/path/to/source"  # Change this to your source file or directory path
url = "http://localhost:8050/uploadfile/"  # Change this to the actual URL of your REST endpoint
results = upload_files_from_source(filedrawer, "x/Users/randolphhill/Documents/uploadfiles", url)
for result in results:
    print(result)

results = upload_files_from_source("SINGLEFILE", "/Users/xrandolphhill/Documents/uploadfiles/D11-1024.pdf", url)
for result in results:
    print(result)
"""

import requests
import os
import glob

def serverupload(filedrawer, filedir):
    server_url = os.getenv("GOVBOTIC_ADMIN_SERVER", "http://localhost:8050") + "/uploadfile/"
    headers = {'Content-Type': 'multipart/form-data'}
    uploaded_files = []

    def upload(file_path):
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            files = {'files': (filename, f)}
            data = {'filedrawer': filedrawer}
            response = requests.post(server_url, files=files, data=data)
            if response.status_code == 200:
                print(f"Successfully uploaded {filename}")
                uploaded_files.append(filename)
            else:
                print(f"Failed to upload {filename}: {response.text}")

    # Check if filedir is a file or directory
    if os.path.isfile(filedir):
        upload(filedir)
    elif os.path.isdir(filedir):
        # List of desired file extensions
        extensions = ['.pdf', '.txt', '.docx', '.md', '.html', '.htm']
        # Find and upload files with the specified extensions
        for ext in extensions:
            for file_path in glob.glob(os.path.join(filedir, f'*{ext}')):
                upload(file_path)
    else:
        print("The provided path is neither a file nor a directory.")

    # Optionally return the list of uploaded files
    return uploaded_files

# Example usage
filedrawer = "Cambodia"
filedir = "./docs/nutrients-14-01183.pdf"
uploaded_files = serverupload(filedrawer, filedir)
print("Uploaded files:", uploaded_files)


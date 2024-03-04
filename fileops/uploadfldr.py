import requests
import os
import glob

def serverupload(filedrawer, filedir):
    server_url = os.getenv("GOVBOTIC_ADMIN_SERVER", "http://localhost:8050") + "/uploadfile/"
    uploaded_files = []
    error_messages = []

    def upload(file_path):
        filename = os.path.basename(file_path)
        try:
            with open(file_path, 'rb') as f:
                files = {'files': (filename, f)}
                data = {'filedrawer': filedrawer}
                response = requests.post(server_url, files=files, data=data)
                if response.status_code == 200:
                    print(f"Successfully uploaded {filename}")
                    uploaded_files.append(filename)
                else:
                    print(f"Failed to upload {filename}: {response.text}")
                    error_messages.append(f"Failed to upload {filename}: {response.text}")
        except Exception as e:
            print(f"Error uploading {filename}: {e}")
            error_messages.append(f"Error uploading {filename}: {str(e)}")

    try:
        if os.path.isfile(filedir):
            upload(filedir)
        elif os.path.isdir(filedir):
            extensions = ['.pdf', '.txt', '.docx', '.md', '.html', '.htm']
            for ext in extensions:
                for file_path in glob.glob(os.path.join(filedir, f'*{ext}')):
                    upload(file_path)
        else:
            return {"error": "The provided path is neither a file nor a directory."}
    except Exception as e:
        return {"error": str(e)}

    if error_messages:
        return {"uploaded_files": uploaded_files, "errors": error_messages}
    else:
        return {"uploaded_files": uploaded_files, "message": "All files uploaded successfully."}

# Example usage
"""
filedrawer = "YourFileDrawerName"
filedir = "/path/to/your/file/or/directory"
result = serverupload(filedrawer, filedir)
print(result)
"""


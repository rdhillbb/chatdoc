import os, sys
import magic
import requests
from urllib.parse import urlparse, unquote
from tqdm import tqdm

sys.path.append("../")
from fileops.onlinedownload import clean_html


def is_html_file(file_path):
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(file_path)
    return mime_type == "text/html"


def is_valid_download_url(url) -> bool:
    # Parse the URL
    parsed_url = urlparse(url)

    # Check if the scheme is valid for downloading (http, https, ftp, file, etc.)
    valid_schemes = ("http", "https", "ftp", "file")  # Add more schemes if needed
    if parsed_url.scheme and parsed_url.scheme.lower() in valid_schemes:
        return True

    return False


def generate_filename_from_url(url):
    parsed_url = urlparse(unquote(url))
    filename = parsed_url.netloc + parsed_url.path
    filename = filename.replace("/", "-")
    if not filename.endswith(".htm") and not filename.endswith(".html"):
        filename += ".txt"
    return filename


def download_file(url, user_agent="Mozilla/5.0") -> str:
    headers = {"User-Agent": user_agent}

    try:
        with requests.get(url, headers=headers, stream=True) as response:
            response.raise_for_status()

            # Try to extract filename from Content-Disposition header if available
            content_disposition = response.headers.get("Content-Disposition")
            if content_disposition:
                # If the filename is found in the header, extract it
                filename = content_disposition.split("filename=")[-1].strip('"')
            else:
                # Extract the filename from the URL or set a default
                filename = os.path.basename(
                    urlparse(unquote(url)).path
                ) or generate_filename_from_url(url)
                root, ext = os.path.splitext(filename)
                if not ext:
                    filename = generate_filename_from_url(url)
            # Adjust the filename if it's empty (for URLs ending with a slash)
            if filename == "":
                filename = "downloaded_content"

            # Specify the directory where the file will be saved
            directory = os.path.join(
                os.environ.get("GOVBOTIC_FILE_SANDBOX", "."), "bottomDrawer"
            )
            os.makedirs(directory, exist_ok=True)

            file_path = os.path.join(directory, filename)

            # Download the file with progress indication
            total_size_in_bytes = int(response.headers.get("content-length", 0))
            progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
            with open(file_path, "wb") as file:
                for data in response.iter_content(1024):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()
            if is_html_file(file_path):
                print("THE FILE IS HTML TYPE: ",file_path)
                print("")
                file_path = clean_html(file_path)
            else:
               print("THE FILE IS NOT TYPE HTMLE: ",file_path)
               print("")
            return os.path.abspath(file_path)

    except requests.exceptions.RequestException as e:
        print(f"Error occurred during file download: {str(e)}")
        return ""


def upload_fileadmin(filedrawer, file_url):
    # Retrieve the server URL from an environment variable
    server_url = os.getenv("GOVBOTIC_ADMIN_SERVER", "http://localhost:8050")

    # Append the specific endpoint to the server URL
    url = f"{server_url}/ingestlocalweb/"

    data = {"request": "upload", "filedrawer": filedrawer, "filename": file_url}

    response = requests.post(
        url, json=data, headers={"Content-Type": "application/json"}
    )

    # Check if the request was successful
    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Error:", response.status_code, response.text)

"""
Test CODE
# Below is used for testing.
#upload_fileadmin("FINAL", "https://www.smashingmagazine.com/2017/05/long-scrolling/")
urllist = [
 "https://www.smashingmagazine.com/2017/05/long-scrolling/",
  "https://www.webmd.com/vitamins/ai/ingredientmono-300/garlic",
  "https://arxiv.org/pdf/2201.11903.pdf",
  "https://sam.gov/api/prod/opps/v3/opportunities/resources/files/1413e32acf2245dbb08f8f00088ce5f4/download?&token="
]
for ur in urllist:
   downloaded_file_path = download_file(ur)
   print(f"File downloaded to: {downloaded_file_path}")
print(is_valid_download_url("https://sam.gov/api/prod/opps/v3/opportunities/resources/files/1413e32acf2245dbb08f8f00088ce5f4/download?&token="))
"""

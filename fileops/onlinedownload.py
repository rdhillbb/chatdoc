import requests
import os
from urllib.parse import urlparse
from tqdm import tqdm
from bs4 import BeautifulSoup
import sys
import time


def is_valid_download_url(url) -> bool:
    parsed_url = urlparse(url)
    valid_schemes = ("http", "https", "ftp", "file")
    if parsed_url.scheme and parsed_url.scheme.lower() in valid_schemes:
        return True
    return False


def download_fl1(url, user_agent="Mozilla") -> str:
    headers = {"User-Agent": user_agent}
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()

        parsed_url = urlparse(url)
        file_name = os.path.basename(parsed_url.path)
        if not file_name.endswith(".pdf"):
            file_name = "downloaded_document.html"

        directory = os.path.join(
            os.environ.get("GEPPETTO_FILE_CABINET", "."), "bottomDrawer"
        )
        os.makedirs(directory, exist_ok=True)

        file_path = os.path.join(directory, file_name)
        total_size = int(response.headers.get("Content-Length", 0))

        with open(file_path, "wb") as file, tqdm(
            total=total_size, unit="B", unit_scale=True, desc=file_name, ncols=80
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                progress_bar.update(len(chunk))

        if not file_name.endswith(".pdf"):
            file_path = clean_html(file_path)

        return os.path.abspath(file_path)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during file download: {str(e)}")
        return f"Error occurred during file download: {str(e)}"


def clean_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    clean_text = soup.get_text()
    clean_file_path = file_path.replace(".", ".clean.html")

    with open(clean_file_path, "w", encoding="utf-8") as file:
        file.write(clean_text)

    os.remove(file_path)
    print(clean_file_path)
    return clean_file_path


import requests
import re
from urllib.parse import urlparse, unquote


def download_contenti1(url, user_agent="Mozilla"):
    headers = {"User-Agent": user_agent}
    response = requests.get(url, headers=headers, stream=True)

    # Check if the response is successful
    if response.status_code == 200:
        content_type = response.headers.get("Content-Type", "").lower()
        content_disposition = response.headers.get("Content-Disposition", "")

        # Attempt to extract filename from Content-Disposition header if present
        filename = None
        if "filename=" in content_disposition:
            filename = re.findall('filename="?(.+)"?', content_disposition)[0]
            filename = unquote(filename)  # Decode URL-encoded filename
        elif content_type == "application/pdf":
            # Default PDF filename if URL is a direct PDF link but no filename is provided
            filename = urlparse(url).path.split("/")[-1] or "downloaded_file.pdf"

        # Determine the appropriate action based on Content-Type
        if content_type == "application/pdf" or filename:
            if not filename.endswith(".pdf"):
                filename += ".pdf"  # Ensure PDF files have the correct extension
            file_type = "PDF"
        elif "html" in content_type:
            filename = urlparse(url).path.split("/")[-1] or "downloaded_page.html"
            file_type = "HTML"
        else:
            print(
                "The content is neither PDF nor HTML, or a filename could not be determined."
            )
            return

        # Save the content to a file
        directory = os.path.join(
            os.environ.get("GOVBOTIC_FILE_SANDBOX", "."), "bottomDrawer"
        )
        os.makedirs(directory, exist_ok=True)

        file_path = os.path.join(directory, filename)

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"{file_type} content downloaded: {filename}")
    else:
        print(f"Failed to download: Status code {response.status_code}")


def main():
    url = input("Enter the URL of the PDF or HTML file to download: ")

    if is_valid_download_url(url):
        try:
            downloaded_file_path = download_file(url)
            print(f"File downloaded successfully. Saved at {downloaded_file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Invalid URL for downloading.")

"""
urls = [
    "https://sam.gov/api/prod/opps/v3/opportunities/resources/files/1413e32acf2245dbb08f8f00088ce5f4/download?&token=",
    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4103721/",
    "https://arxiv.org/pdf/2201.11903.pdf",
]

for url in urls:
    download_content(url)
main()
"""
# if __name__ == "__main__":
#    main()

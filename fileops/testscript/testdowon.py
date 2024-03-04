import requests
import re
from urllib.parse import urlparse, unquote

def download_content(url, user_agent="Mozilla"):
    headers = {"User-Agent": user_agent}
    response = requests.get(url, headers=headers, stream=True)

    # Check if the response is successful
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type', '').lower()
        content_disposition = response.headers.get('Content-Disposition', '')
        
        # Attempt to extract filename from Content-Disposition header if present
        filename = None
        if 'filename=' in content_disposition:
            filename = re.findall('filename="?(.+)"?', content_disposition)[0]
            filename = unquote(filename)  # Decode URL-encoded filename
        elif content_type == 'application/pdf':
            # Default PDF filename if URL is a direct PDF link but no filename is provided
            filename = urlparse(url).path.split('/')[-1] or "downloaded_file.pdf"
        
        # Determine the appropriate action based on Content-Type
        if content_type == 'application/pdf' or filename:
            if not filename.endswith('.pdf'):
                filename += '.pdf'  # Ensure PDF files have the correct extension
            file_type = 'PDF'
        elif 'html' in content_type:
            filename = urlparse(url).path.split('/')[-1] or "downloaded_page.html"
            file_type = 'HTML'
        else:
            print('The content is neither PDF nor HTML, or a filename could not be determined.')
            return

        # Save the content to a file
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f'{file_type} content downloaded: {filename}')
    else:
        print(f"Failed to download: Status code {response.status_code}")

# Example usage:
urls = [
    "https://sam.gov/api/prod/opps/v3/opportunities/resources/files/1413e32acf2245dbb08f8f00088ce5f4/download?&token=",
    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4103721/",
    "https://arxiv.org/pdf/2201.11903.pdf"
]

for url in urls:
    download_content(url)


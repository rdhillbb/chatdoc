import fitz
from langchain_core.documents import Document

def sharwood_slipter(file_path):
    docs = []
    totalwords = 0
    largestPage = 0
    with fitz.open(file_path) as pdf_file:
        num_pages = pdf_file.page_count
        for page_num in range(num_pages):
            # print("Page: ", page_num)
            pagenumber = "Page:" + str(page_num) + " "
            # Get the current page
            page = pdf_file[page_num]
            # Get the text from the current page
            page_text = page.get_text()
            # Append the text to context
            page_text = page_text.replace("\n", " ")
            page_text = page_text.replace("    ", " ")
            docs.append(Document(page_content=pagenumber + page_text))
            # print(page_text)
    return docs

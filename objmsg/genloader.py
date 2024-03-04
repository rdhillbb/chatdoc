from langchain_community.document_loaders import UnstructuredHTMLLoader, TextLoader
from langchain_community.document_loaders import CSVLoader, UnstructuredExcelLoader
from langchain_community.document_loaders import (
    UnstructuredPowerPointLoader,
    PyPDFLoader,
)
from langchain_community.document_loaders import Docx2txtLoader


class GMyLoader:
    def __init__(self, file_path, **kwargs):
        if file_path.endswith(".html"):
            self.loader = UnstructuredHTMLLoader(file_path, **kwargs)
        elif file_path.endswith(".htm"):
            self.loader = TextLoader(file_path, **kwargs)
        elif file_path.endswith(".csv"):
            self.loader = CSVLoader(file_path, **kwargs)
        elif file_path.endswith(".txt"):
            self.loader = TextLoader(file_path, **kwargs)
        elif file_path.endswith(".pdf"):
            self.loader = PyPDFLoader(file_path, **kwargs)
        elif file_path.endswith(".xlsx"):
            self.loader = UnstructuredExcelLoader(file_path, **kwargs)
        elif file_path.endswith(".docx"):
            self.loader = Docx2txtLoader(file_path, **kwargs)
        elif file_path.endswith(".ppt"):
            self.loader = UnstructuredPowerPointLoader(file_path, **kwargs)
        else:
            raise ValueError("Unsupported file extension")

    def load(self):
        return self.loader.load()

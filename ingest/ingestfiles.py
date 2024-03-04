import os
import sys
from typing import List
from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
import glob
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
import shutil

sys.path.append("../")

from objmsg.genloader import GMyLoader


def setupingest(filecabinet, filepath):
    # Get the base directory path from the environment variable
    base_dir = os.getenv("GOVBOTIC_INGESTION_STORAGE")
    if not base_dir:
        raise ValueError(
            "Environment variable 'GOVBOTIC_INGESTION_STORAGE' is not set."
        )

    # Extract the name of the file from the filepath
    filename = os.path.basename(filepath)

    # Remove the file extension to use the name for the directory creation
    file_name_without_extension = os.path.splitext(filename)[0]

    # Construct the full path where the directory will be created
    full_path = os.path.join(base_dir, filecabinet, file_name_without_extension)

    # Create the directory if it does not exist
    os.makedirs(full_path, exist_ok=True)

    # Construct the new file path in the newly created directory
    new_file_path = os.path.join(full_path, filename)

    # Move the file to the new directory
    shutil.copy(filepath, new_file_path)

    return new_file_path


from langchain_openai import OpenAIEmbeddings


def ing_singlefile(
    file_path, chunksize: int = 1000, overlap: int = 300
) -> Optional[str]:
    try:
        file_dir = os.path.dirname(file_path)
        persist_directory = os.path.join(file_dir, "chroma_db")
        embeddings = OpenAIEmbeddings()
        loader = GMyLoader(file_path)
        print(file_dir)
        print(persist_directory)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunksize, chunk_overlap=overlap
        )
        docs = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()
        db2 = Chroma.from_documents(
            docs, embeddings, persist_directory=persist_directory
        )
        db2.persist()
        return "Complete"
    except Exception as e:
        return f"ERROR: {str(e)}"


def copy_file_to_new_dir(file_path) -> str:
    # filepath = file_path.replace(phrase, "")
    base_name = os.path.basename(file_path)
    file_name, _ = os.path.splitext(base_name)
    new_dir = os.path.join(
        os.environ["GEPPETTO_FILE_CABINET"], "middleDrawer", file_name
    )

    os.makedirs(new_dir, exist_ok=True)

    new_file_path = os.path.join(new_dir, base_name)
    shutil.copy(file_path, new_file_path)
    return new_file_path


def rename_file(file_path):
    # check if the file is a .pdf and has exactly one dot before '.pdf'
    if file_path.endswith(".pdf") and file_path.count(".") == 2:
        # get the directory path and the filename
        directory, filename = os.path.split(file_path)
        # replace the first '.' with '_' in the filename
        new_filename = filename.replace(".", "_", 1)
        # rename the file
        os.rename(file_path, os.path.join(directory, new_filename))

        return os.path.join(directory, new_filename)
    else:
        return file_path

"""
filecabinet = "GARLIC"
filelocation ="/Users/randolphhill/Downloads/ajp-4-001.pdf"
filetoingest = setupingest(filecabinet, filelocation)
ingested_File=ing_singlefile(filetoingest)
print(ingested_File)
"""

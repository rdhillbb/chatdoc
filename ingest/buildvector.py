from langchain_community.document_loaders import DirectoryLoader
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def ing_dirconsolidate(dir_path: str, chunksize: int = 1000, overlap: int = 300) -> str:
    try:
        persist_directory = f"{dir_path}/chroma_db"
        loader = DirectoryLoader(dir_path, glob="./*.*")
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunksize, chunk_overlap=overlap
        )
        docs = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()
        # persist_directory = os.path.dirname(os.path.abspath(fileName))+"/chroma_db"
        db2 = Chroma.from_documents(
            docs, embeddings, persist_directory=persist_directory
        )
        db2.persist()
        return "Complete"
    except Exception as e:
        return f"ERROR: {str(e)}"


ing_dirconsolidate(
    "/Users/randolphhill/govbotics/deepinfra/Pansolusi/fifserver/ingestion/DOCUMENTS/fifdocs"
)

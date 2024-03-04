from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
persist_directory = (
    "/Users/randolphhill/govbotics/deepinfra/Pansolusi/fifserver/ingestion/DOCUMENTS/Amortization HILL"
    + "/chroma_db"
)
embeddings = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
print(vectordb.similarity_search("Randolph Hill's mortgage amount"))

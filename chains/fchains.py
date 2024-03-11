import bs4
import os
from langchain_community.document_loaders import DirectoryLoader
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import sys, time, threading
from langchain_community.llms import DeepInfra

sys.path.append("../")

from config.llmload import  get_modelInstance
from objmsg.genloader import GMyLoader
from objmsg.fprompt import osprompt

# Cheap Initialization at startup
prompt = hub.pull("rlm/rag-prompt")


def is_valid_directory(path):
    # Check if the path exists and is a directory
    if os.path.exists(path) and os.path.isdir(path):
        print(f"The path '{path}' is a valid directory.")
        return True
    else:
        print(f"The path '{path}' is not a valid directory.")
        return False


def spinner():
    global spinning
    spinner_chars = ["|", "/", "-", "\\"]
    while spinning:
        for char in spinner_chars:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write("\b")
    sys.stdout.write("\b")


def create_retriever_from_url(url):
    # Load, chunk and index the contents of the URL.
    loader = WebBaseLoader(
        web_paths=(url,),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("post-content", "post-title", "post-header")
            )
        ),
    )
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=800)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    # Retrieve and return the retriever.
    retriever = vectorstore.as_retriever()
    return retriever


def createQchain(path):
    print("Create Victor DB")
    loader = GMyLoader(path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=600)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()
    #
    # LLM & Prompt Setup
    llmSetec = os.environ.get("GOVBOTIC_LLM")
    # prompt = hub.pull("rlm/rag-prompt")

    # ADD YOUR MODEL HERE
    if llmSetec == "iXOpenAI":
        prompt.messages[0].prompt.template = osprompt

        llm = DeepInfra(model_id="mistralai/Mixtral-8x7B-Instruct-v0.1")
        llm.model_kwargs = {
            "temperature": 0.6,
            "repetition_penalty": 1.2,
            "max_new_tokens": 8900,
            "top_p": 0.3,
        }
    else:
        llm = ChatOpenAI(model_name="gpt-4-0125-preview", temperature=0.6)
    llm = getmodelInstance()
    # Use the retriever to fetch relevant content

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # resp = rag_chain.invoke("What is this document about ?")
    # print(resp)
    return rag_chain


def createDchain(file: str):
    print("Create Victor DB")

    if is_valid_file_path(file):
        loader = GMyLoader(file)
        docs = loader.load()
    else:
        loader = DirectoryLoader(file, glob="**/*.pdf")
        docs = loader.load()

    print()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=600)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()

    # LLM & Prompt Setup
    llmSetec = os.environ.get("GOVBOTIC_LLM")
    # prompt = hub.pull("rlm/rag-prompt")

    # ADD YOUR MODEL HERE
    if llmSetec != "OpenAI":
        prompt.messages[0].prompt.template = osprompt

        llm = DeepInfra(model_id="mistralai/Mixtral-8x7B-Instruct-v0.1")
        llm.model_kwargs = {
            "temperature": 0.6,
            "repetition_penalty": 1.2,
            "max_new_tokens": 8900,
            "top_p": 0.3,
        }
    else:
        llm = ChatOpenAI(model_name="gpt-4-0125-preview", temperature=0.6)
    # Use the retriever to fetch relevant content

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


prompt = hub.pull("rlm/rag-prompt")


def createLchain(drawer: str):
    print("Loading VB " + drawer)
    persist_directory = env_var_value = (
        os.getenv("GOVBOTIC_INGESTION_STORAGE") + "/" + drawer + "/chroma_db"
    )
    if not os.path.isdir(persist_directory):
        raise MyCustomException("Folder or Document does not exist")
    print("FILE DRAWER:", persist_directory)
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        persist_directory=persist_directory, embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever()

    # LLM & Prompt Setuop
    llmSetec = os.environ.get("GOVBOTIC_LLM")
    llm = get_modelInstance()
    # ADD YOUR MODEL HERE
    if "OpenAI" not in llmSetec:
        prompt.messages[0].prompt.template = osprompt
    else:
        prompt.messages[0].prompt.template = openaiprompt

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# chain = createLchain("Arixiv/2305.10601")
# print(chain.invoke("What is the document about? If you do now know say you do not know."))

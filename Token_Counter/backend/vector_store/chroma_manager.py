import os
from langchain_chroma import Chroma
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)
from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)
from langchain_core.documents import Document

import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DOC_FOLDER = os.path.join(
    BASE_DIR,
    "documents"
)
DB_FOLDER = "chroma_db"

embedding_model = (
    HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )
)


def build_vector_store():

    documents = []

    if not os.path.exists(DOC_FOLDER):
        return

    for file in os.listdir(DOC_FOLDER):

        path = os.path.join(DOC_FOLDER,file)

        with open(path,"r",encoding="utf-8") as f:

            text = f.read()

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": file
                }))

    splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
    )

    chunks = splitter.split_documents(
        documents
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=DB_FOLDER)

    return vector_store


def load_vector_store():

    return Chroma(
        persist_directory=DB_FOLDER,
        embedding_function=
        embedding_model
    )
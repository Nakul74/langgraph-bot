from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers.multi_query import MultiQueryRetriever
# from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from src import models

compressor = LLMChainExtractor.from_llm(models.openai_llm)

def create_retriever(directory_path):
    loader = DirectoryLoader(directory_path, show_progress=True, use_multithreading=True, silent_errors=True, loader_kwargs={"autodetect_encoding": True})
    docs_list = loader.load()

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=500, chunk_overlap=50
    )
    doc_splits = text_splitter.split_documents(docs_list)

    # Add to vectorDB
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        embedding=models.openai_embedding,
    )

    retriever = MultiQueryRetriever.from_llm(retriever=vectorstore.as_retriever(search_kwargs={"k": 10}), llm=models.openai_llm)
    # compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)

    return retriever
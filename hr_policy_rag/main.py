import os

from langchain_aws import BedrockEmbeddings
from langchain_classic.chains.llm import LLMChain
from langchain_community.document_loaders import  PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_classic.indexes import  VectorstoreIndexCreator
from langchain_aws import  BedrockLLM

def hr_index_and_store():

    data_loader=PyPDFLoader('https://www.upl-ltd.com/images/people/downloads/Leave-Policy-India.pdf')
    data_split=RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " ", ""], chunk_size=1000, chunk_overlap=100)

    # data_test=data_loader.load_and_split()
    # print(len(data_test))


    data_embeddings=BedrockEmbeddings(
        # credentials_profile_name="default",
        model_id='amazon.titan-embed-text-v2:0',
        # region_name='us-east-1'
    )
    data_index=VectorstoreIndexCreator(
        text_splitter=data_split,
        embedding=data_embeddings,
        vectorstore_cls=FAISS
    )
    db_index=data_index.from_loaders([data_loader])

    print("hr_index_and_store ===> Done")
    print(db_index)
    return db_index

def hr_llm():
    llm=BedrockLLM(
        # region_name='us-east-1',
        model='amazon.titan-text-lite-v1',
        model_kwargs={
            "temperature": 0.1})
    print("hr_llm ===> Done")
    return  llm

def hr_rag_query(index,query_text):
    myLLM=hr_llm()
    hr_rag_query=index.query(question=query_text,llm=myLLM)
    print("hr_rag_query ===> Done")
    return  hr_rag_query



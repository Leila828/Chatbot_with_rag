import os
from dotenv import load_dotenv


from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import ChatPromptTemplate

from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFaceHub
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()  # Load environment variables from .env file

# Access the API token
HUGGINGFACEHUB_API_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')
def chat_with_rag(urls,query,pdf):
    all_docs = []

    for url in urls:
            loader = WebBaseLoader(url)
            data = loader.load()
            all_docs.extend(data)


    loader = PyPDFLoader(pdf)

    data_pdf = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(all_docs)

    text_splitter_pdf = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts_pdf = text_splitter_pdf.split_documents(data_pdf)

    all_texts = texts + texts_pdf

    embeddings = HuggingFaceEmbeddings( model_name="sentence-transformers/all-mpnet-base-v2" )
    db = FAISS.from_documents(all_texts, embeddings)
    retriever = db.as_retriever()

    template = """Answer the question based only on the following context:

    {context}
if you don't know the answer, say 'I don't know
    Question: {question}

    """
    prompt = ChatPromptTemplate.from_template(template)

    llm = HuggingFaceHub(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        task="text-generation",
        model_kwargs={"temperature": 0.1, "max_length": 512},
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
    )


    chain_type_kwargs = {"prompt": prompt}
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever,chain_type_kwargs=chain_type_kwargs)


    # Test the chatbot
    response = chain.run(query)

    return response
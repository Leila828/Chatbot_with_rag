import os
from dotenv import load_dotenv
import requests

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
    # Handle empty query case
    if not query.strip():
        return "Please provide a valid query."

    all_docs = []
    # Handle URLs and fetch content
    for url in urls:
        try:
            loader = WebBaseLoader(url)
            data = loader.load()
            if not data:
                raise ValueError(f"No content found at URL: {url}")
            all_docs.extend(data)
        except requests.exceptions.RequestException as e:
            print(f"Failed to load content from {url}: {e}")
        except Exception as e:
            print(f"Error processing URL {url}: {e}")

    # Handle PDF loading
    try:
        if not os.path.exists(pdf):
            raise FileNotFoundError(f"PDF file '{pdf}' not found.")
        loader = PyPDFLoader(pdf)
        data_pdf = loader.load()
        if not data_pdf:
            raise ValueError("The PDF file is empty or invalid.")
    except FileNotFoundError as e:
        print(e)
        return "Error: PDF file not found."
    except Exception as e:
        print(f"Error processing PDF file '{pdf}': {e}")
        return "Error: Failed to process PDF."


    # Split texts from URLs and PDF
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(all_docs)

    text_splitter_pdf = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts_pdf = text_splitter_pdf.split_documents(data_pdf)

    all_texts = texts + texts_pdf
    # Embed and retrieve content
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        db = FAISS.from_documents(all_texts, embeddings)
        retriever = db.as_retriever()
    except Exception as e:
        print(f"Error with embeddings or vector store: {e}")
        return "Error: Failed to process embeddings or vector store."

    template = """Based only on the following context, provide a concise answer to the question.Don’t justify your answers. Don’t give information not mentioned in the CONTEXT INFORMATION. If the answer is not available in the context, respond with "I don't know. "

Context: {context}
    
Question: {question}
Answer:

    """
    prompt = ChatPromptTemplate.from_template(template)

    # Load the LLM from HuggingFace
    try:
        llm = HuggingFaceHub(
            repo_id="HuggingFaceH4/zephyr-7b-beta",
            task="text-generation",
            model_kwargs={"temperature": 0.1, "max_length": 512},
            huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
        )
    except Exception as e:
        print(f"Error initializing HuggingFace model: {e}")
        return "Error: Failed to initialize LLM."

    # Create the chain and run the query
    chain_type_kwargs = {"prompt": prompt}
    try:
        chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever,chain_type_kwargs=chain_type_kwargs)


        # Test the chatbot
        response = chain.run(query)

        # Process and clean the response
        answer = response.split("Answer:")[-1].strip()


        # Return the concise question and answer
        return f"Question: {query}\nAnswer: { answer}"

    except Exception as e:
        print(f"Error during query execution: {e}")
        return "Error: Failed to execute query."


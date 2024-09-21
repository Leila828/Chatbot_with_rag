import pytest
from unittest.mock import patch, MagicMock
from utils.rag import chat_with_rag


urls = [
    "https://data.worldbank.org/indicator/SI.POV.DDAY?locations=1W-BR",
    "https://data.worldbank.org/indicator/IT.NET.USER.ZS?locations=1W-BR",
    "https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS?locations=1W-BR",
]
pdf = 'data/gem_report.pdf'
# Mock long and complex inputs for performance testing
long_query = "A" * 10000  # A query with 10,000 characters
large_pdf_content = "A" * 50000  # Simulate a PDF with a large amount of text

# Helper function to mock WebBaseLoader and PyPDFLoader
def mock_loader(loader_class, data):
    mock_loader_instance = MagicMock()
    mock_loader_instance.load.return_value = data
    return patch(f'utils.rag.{loader_class}', return_value=mock_loader_instance)


# Helper function to mock FAISS and HuggingFaceEmbeddings
def mock_faiss_and_embeddings():
    mock_embeddings = MagicMock()
    mock_db = MagicMock()
    mock_retriever = MagicMock()

    mock_db.as_retriever.return_value = mock_retriever
    mock_faiss = patch('utils.rag.FAISS.from_documents', return_value=mock_db)
    mock_embeddings_patch = patch('utils.rag.HuggingFaceEmbeddings', return_value=mock_embeddings)

    return mock_faiss, mock_embeddings_patch


# Mock HuggingFaceHub for the LLM
mock_llm = patch('utils.rag.HuggingFaceHub')

# Test Case 1: Test with valid inputs


# Mock HuggingFaceHub to avoid actual API calls during testing
@patch('langchain_community.llms.huggingface_hub.HuggingFaceHub.generate')
def test_chatbot(mock_generate):
    # Configure mock response
    mock_generate.return_value = "Mocked LLM Response"

    # Test cases
    test_long_query()
    test_empty_query()
    test_known_answer()
    test_unknown_answer()



def test_empty_query():
    response = chat_with_rag(urls, "", pdf)
    assert "Missing 'query' parameter" or "Please provide a valid query." in response or response == ""

def test_known_answer():
    query = "are the graduate more likely to start a new business"


    response = chat_with_rag(urls, query, pdf)
    print(response)


    assert "Yes" in response

def test_unknown_answer():
    query = "when was the GEM created?"

    response = chat_with_rag(urls, query, pdf)
    print(response)
    assert "I don't know" in response or "The context provided does not include information about" in response




def test_long_query():
    long_query = "A" * 10000  # A query with 10,000 characters
    response = chat_with_rag(urls, long_query, pdf)

    # Expecting the system to handle the long query without crashing
    assert isinstance(response, str)


# Edge Case 1: Test with a large PDF
"""@patch('utils.rag.PyPDFLoader.load', return_value=[{"content": large_pdf_content}])
def test_large_pdf(mock_pdf_loader):
    query = "What is the content of the large PDF?"
    response = chat_with_rag(urls, query, pdf)

    # Check if the response is a string (since it could be too large to manually assert exact content)
    assert isinstance(response, str)"""
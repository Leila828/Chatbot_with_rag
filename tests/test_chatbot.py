import pytest
from unittest.mock import patch, MagicMock
from utils.rag import chat_with_rag


urls = [
    "https://data.worldbank.org/indicator/SI.POV.DDAY?locations=1W-BR",
    "https://data.worldbank.org/indicator/IT.NET.USER.ZS?locations=1W-BR",
    "https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS?locations=1W-BR",
]
pdf = 'data/GEM.pdf'


# Mock HuggingFaceHub to avoid actual API calls during testing
@patch('langchain_community.llms.huggingface_hub.HuggingFaceHub.generate')
def test_chatbot(mock_generate):
    # Configure mock response
    mock_generate.return_value = "Mocked LLM Response"

    # Test cases
    test_empty_query()
    test_known_answer()
    test_unknown_answer()


def test_empty_query():
    response = chat_with_rag(urls, "", pdf)
    assert "I don't know" in response or response == ""

def test_known_answer():
    query = "does the level of entreneurship has an impact on nation economic"

    response = chat_with_rag(urls, query, pdf)
    start_index = response.find("if you don't know the answer, say 'I don't know") + len("if you don't know the answer, say 'I don't know")

    assert "Yes" in response[start_index:]

def test_unknown_answer():
    query = "what is the name of my father"

    response = chat_with_rag(urls, query, pdf)
    start_index = response.find("if you don't know the answer, say 'I don't know") + len("if you don't know the answer, say 'I don't know")

    assert "I don't know" in response[start_index:]

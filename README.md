# Chatbot_with_rag API
This repository contains a chatbot that uses Hugging Face Hub and Langchain for Retrieval-Augmented Generation (RAG). The chatbot fetches data from the World Bank, GEM reports, and other sources and generates responses using HuggingFace models.

## Project Features:
*     Retrieves data from World Bank datasets and GEM PDF reports.
*     Implements Retrieval-Augmented Generation (RAG) using Langchain.
*     Uses HuggingFace LLMs for text generation.
*     Includes robust error handling for network issues and invalid input.
*     API with endpoints for user interaction.
*     Automatic PDF download from GEM Consortium.
*     Unit tests for chatbot functionality.


## This project uses 
    -Python
    -Flask
    -HuggingFace
    -langchain
## Installation
To run the chatbot locally, you will need to install the following libraries:
    
* Clone the repository:
```bash
git clone https://github.com/your-repo/chatbot_with_rag.git
cd chatbot_with_rag
```
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```

```bash
pip install -r requirements.txt
```
## Usage

To run the chatbot, you will need to provide a Hugging Face Hub API token. You can do this by setting the following environment variables:
```bash export HUGGINGFACEHUB_API_TOKEN= TOKEN```

To run the development server, run the following commands in the git bash terminal:
```bash
export FLASK_APP=main.py
export FLASK_ENV=development
export FLASK_DEBUG=true
# For http connection
flask run --reload
```

After running the above commands, the Flask app will be available at:
http://127.0.0.1:5000

## API Endpoints
POST /query: The main endpoint for interacting with the chatbot.

* Request: 
{
  "query": "Your question here"
}

* Response:
{
  "response": "Chatbot response here"
}
 ## Data Fetching
The project automatically fetches data from the following sources:

*     World Bank Datasets:
*     Poverty headcount ratio
*     Individuals using the Internet
*     Unemployment rate
*     GEM Consortium PDF Report: Automatically downloads and processes the first PDF from the GEM reports page.

## Testing
Unit tests are available for testing chatbot functionality.

To run the tests, simply use pytest:

```bash
pytest

```
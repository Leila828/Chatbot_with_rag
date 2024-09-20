# Chatbot_with_rag API
This repository contains a chatbot function uses  the Hugging Face Hub and Langchain.

## This project uses 
    -Python
    -Flask
    -HuggingFace
    -langchain
## Installation
To run the chatbot locally, you will need to install the following libraries:
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
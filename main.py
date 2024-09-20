# This is a sample Python script.
from flask import Flask, request, jsonify
from utils.rag import chat_with_rag
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400


    urls = [
        "https://data.worldbank.org/indicator/SI.POV.DDAY?locations=1W-BR",
        "https://data.worldbank.org/indicator/IT.NET.USER.ZS?locations=1W-BR",

    ]
    pdf_path = "data/GEM.pdf"  # Replace with your actual PDF path
    response = chat_with_rag(urls, query, pdf_path)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_VERSION = "2022-06-28"

@app.route("/get-snippet", methods=["GET"])
def get_snippet():
    return jsonify({
        "summary": "Buy groceries\nClean fridge\nDeclutter hallway"
    })

@app.route("/")
def root():
    return "Notion Bridge is alive"

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

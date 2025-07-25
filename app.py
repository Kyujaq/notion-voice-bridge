from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_VERSION = "2022-06-28"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json"
}

@app.route("/get-page", methods=["GET"])
def get_page():
    page_id = request.args.get("page_id")
    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=10"
    res = requests.get(url, headers=HEADERS)
    data = res.json()

    blocks = []
    for block in data.get("results", []):
        block_type = block.get("type")
        text = block.get(block_type, {}).get("text", [])
        plain = "".join(t.get("text", {}).get("content", "") for t in text)
        if plain:
            blocks.append(f"- {plain}")
    return jsonify({"summary": "\n".join(blocks)})

@app.route("/query-database", methods=["GET"])
def query_database():
    database_id = request.args.get("database_id")
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    res = requests.post(url, headers=HEADERS)
    data = res.json()

    items = []
    for result in data.get("results", []):
        props = result.get("properties", {})
        title = next(
            (p["title"][0]["text"]["content"]
             for p in props.values() if p["type"] == "title" and p["title"]),
            None
        )
        if title:
            items.append(f"- {title}")
    return jsonify({"summary": "\n".join(items)})

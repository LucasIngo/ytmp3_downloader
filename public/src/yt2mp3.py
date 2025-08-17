# yt2mp3.py
from flask import Flask, request, jsonify, send_from_directory
from downloader import download_mp3, get_suggestion
from utils import sanitize_filename
import yaml, os

app = Flask(__name__, static_folder="../", static_url_path="")

with open("config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
DOWNLOAD_DIR = config.get("download_dir", "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/")
def index():
    return send_from_directory("../", "index.html")

@app.route("/suggest", methods=["POST"])
def suggest():
    data = request.json
    url = data.get("url")
    return get_suggestion(url)

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    return download_mp3(data, DOWNLOAD_DIR)

@app.route("/downloads/<path:filename>")
def serve_file(filename):
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
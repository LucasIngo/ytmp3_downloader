# yt2mp3.py
from flask import Flask, request, jsonify, send_from_directory
from downloader import download_mp3, get_suggestion, download_playlist
from utils import sanitize_filename
import yaml, os, logging, logging_config

logging.getLogger("werkzeug").setLevel(logging.ERROR)
app = Flask(__name__, static_folder="../", static_url_path="")

with open("config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
download_dir = config.get("download_dir", "downloads")
os.makedirs(download_dir, exist_ok=True)

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
    return download_mp3(data, download_dir)

@app.route("/downloads/<path:filename>")
def serve_file(filename):
    return send_from_directory(download_dir, filename, as_attachment=True)

@app.route("/download-playlist", methods=["POST"])
def download_playlist_route():
    data = request.json
    tracks = data.get("tracks", [])
    return download_playlist(tracks, download_dir)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
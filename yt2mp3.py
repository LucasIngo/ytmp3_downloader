from flask import Flask, request, jsonify, send_from_directory, render_template
import os, re, logging
from yt_dlp import YoutubeDL
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

app = Flask(__name__, static_folder="public", static_url_path="")
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "", name)

def update_tags(file_path: str, artist: str, title: str):
    audio = MP3(file_path, ID3=EasyID3)
    audio['artist'] = artist.strip()
    audio['title'] = title.strip()
    audio.save()

@app.route("/")
def index():
    return send_from_directory("public", "index.html")

# --- Schritt 1: Vorschlag holen ---
@app.route("/suggest", methods=["POST"])
def suggest():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"success": False, "message": "Kein YouTube-Link angegeben"})

    ydl_opts = {"quiet": True, "skip_download": True, "noplaylist": True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get("title", "Unbekannter Titel")
        artist = info.get("uploader", "Unbekannter Künstler")

    return jsonify({"success": True, "title": title, "artist": artist})

# --- Schritt 2: Download ---
@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")
    title = data.get("title")
    artist = data.get("artist")
    if not url or not title or not artist:
        return jsonify({"success": False, "message": "Fehlende Daten"})

    safe_title = sanitize_filename(title)
    safe_artist = sanitize_filename(artist)
    filename = f"{safe_artist} - {safe_title}.mp3"
    output_path = os.path.join(DOWNLOAD_DIR, filename)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path.replace(".mp3", ".%(ext)s"),
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "0"},
            {"key": "FFmpegMetadata"}  # <- hier sorgt FFmpeg für ID3-Tags
        ],
        "noplaylist": True,
        "quiet": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        update_tags(output_path, artist, title)
        return jsonify({"success": True, "filename": filename, "path": DOWNLOAD_DIR})
    except Exception as e:
        logging.error(e)
        return jsonify({"success": False, "message": str(e)})

@app.route("/downloads/<path:filename>")
def serve_file(filename):
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


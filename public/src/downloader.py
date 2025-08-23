# downloader.py
from yt_dlp import YoutubeDL
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from flask import jsonify
from utils import sanitize_filename
import os, logging

def get_suggestion(url):
    if not url:
        return jsonify({"success": False, "message": "Kein YouTube-Link angegeben"})
    ydl_opts = {"quiet": True, "skip_download": True, "noplaylist": True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get("title", "Unbekannter Titel")
        artist = info.get("uploader", "Unbekannter Künstler")
    return jsonify({"success": True, "title": title, "artist": artist})

def download_mp3(data, DOWNLOAD_DIR):
    url = data.get("url")
    title = data.get("title")
    artist = data.get("artist")
    if not url or not title or not artist:
        return jsonify({"success": False, "message": "Fehlende Daten"})
    safe_title = sanitize_filename(title)
    safe_artist = sanitize_filename(artist)
    filename = f"{safe_artist} - {safe_title}.mp3"
    output_path = os.path.join(DOWNLOAD_DIR, filename)
    print("Saving to:", output_path)

    # Check if directory exists and is writable
    if not os.path.isdir(DOWNLOAD_DIR):
        print(f"Download directory does not exist: {DOWNLOAD_DIR}")
    elif not os.access(DOWNLOAD_DIR, os.W_OK):
        print(f"No write permission for: {DOWNLOAD_DIR}")
    else:
        print(f"Write permission OK for: {DOWNLOAD_DIR}")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path.replace(".mp3", ".%(ext)s"),
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "0"},
            {"key": "FFmpegMetadata"}
        ],
        "noplaylist": True,
        "quiet": True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        audio = MP3(output_path, ID3=EasyID3)
        audio['artist'] = artist.strip()
        audio['title'] = title.strip()
        #Remove or reset trachnumber
        if 'tracknumber' in audio:
            audio['tracknumber'] = ""
        print(f"suggested output path: {output_path}")
        print(f"suggested download_folder: {DOWNLOAD_DIR}")
        audio.save()
        print(f"File saved at: {output_path}")
        print(f"download_folder: {DOWNLOAD_DIR}")
        if os.path.isfile(output_path):
            print(f"File successfully saved: {output_path}")
        else:
            print(f"File NOT found after saving: {output_path}")
        return jsonify({"success": True, "filename": filename, "path": DOWNLOAD_DIR})
    except Exception as e:
        print(f"Exception occurred: {e}")  # <-- Add this line
        logging.error(e)
        return jsonify({"success": False, "message": str(e)})
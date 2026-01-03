# downloader.py
from yt_dlp import YoutubeDL
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from flask import jsonify
from utils import sanitize_filename
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import os, logging

logger = logging.getLogger(__name__)

def get_suggestion(url):
    if not url:
        return jsonify({"success": False, "message": "Kein YouTube-Link angegeben"})
    
    url = normalize_youtube_url(url)
    logger.debug("Hole Vorschlag für URL")
    ydl_opts = {
        "quiet": True, 
        "skip_download": True, 
        "extract_flat": "in_playlist",
        "no warnings": True
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # Playlist
    if "entries" in info:
        tracks = []
        logger.info("Playlist erkannt (%d Einträge)", len(info["entries"]))
        for entry in info["entries"]:
            if not entry:
                continue
            tracks.append({
                "title": entry.get("title", "Unbekannter Titel"),
                "artist": entry.get("uploader", "Unbekannter Künstler"),
                "url": entry.get("url")
            })

        return jsonify({
            "success": True,
            "type": "playlist",
            "tracks": tracks,
            "normalized_url": url
        })

    logger.info("Einzelvideo erkannt")
    # Einzelvideo
    return jsonify({
        "success": True,
        "type": "single",
        "tracks": [{
            "title": info.get("title", "Unbekannter Titel"),
            "artist": info.get("uploader", "Unbekannter Künstler"),
            "url": url
        }],
        "normalized_url": url
    })

def normalize_youtube_url(url: str) -> str:
    parsed = urlparse(url)

    netloc = parsed.netloc
    if netloc == "music.youtube.com":
        netloc = "www.youtube.com"

    qs = parse_qs(parsed.query)

    clean_qs = {}

    # Video
    if "v" in qs:
        clean_qs["v"] = qs["v"]

    # Playlist (WICHTIG!)
    if "list" in qs:
        clean_qs["list"] = qs["list"]

    return urlunparse((
        parsed.scheme or "https",
        netloc,
        parsed.path,
        parsed.params,
        urlencode(clean_qs, doseq=True),
        ""
    ))

    parsed = urlparse(url)

    # music.youtube.com → www.youtube.com
    netloc = parsed.netloc
    if netloc == "music.youtube.com":
        netloc = "www.youtube.com"

    # Query-Parameter filtern (nur v behalten)
    qs = parse_qs(parsed.query)
    clean_qs = {}
    if "v" in qs:
        clean_qs["v"] = qs["v"]

    return urlunparse((
        parsed.scheme or "https",
        netloc,
        parsed.path,
        parsed.params,
        urlencode(clean_qs, doseq=True),
        ""
    ))

def download_mp3(data, download_dir):
    url = data.get("url")
    url = normalize_youtube_url(url)
    title = data.get("title")
    artist = data.get("artist")
    
    if not url or not title or not artist:
        return jsonify({"success": False, "message": "Fehlende Daten"})
    
    safe_title = sanitize_filename(title)
    safe_artist = sanitize_filename(artist)
    filename = f"{safe_artist} - {safe_title}.mp3"
    output_path = os.path.join(download_dir, filename)
    
    logger.info("Starte download")

    # Check if directory exists and is writable
    if not os.path.isdir(download_dir):
        logger.error("Download directory does not exist: %s", download_dir)
    elif not os.access(download_dir, os.W_OK):
        logger.error("No write permission for: %s", download_dir)
    else:
        logger.error("Write permission OK for: %s", download_dir)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path.replace(".mp3", ".%(ext)s"),
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "0"},
            {"key": "FFmpegMetadata"}
        ],
        "noplaylist": True,
        "quiet": True,
        "logger": logging.getLogger("yt_dlp"),
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
       
        audio.save()
        
        if os.path.isfile(output_path):
            logger.info("File successfully saved: %s", filename)
        else:
            logger.info("File NOT found after saving: %s", output_path)
        
        return jsonify({"success": True, "filename": filename, "path": download_dir})
    except Exception as e:# <-- Add this line
        logging.exception("Fehler beim Download")
        return jsonify({"success": False, "message": "Download fehlgeschlagen"})
    
def download_playlist(tracks, download_dir):
    results = []

    for track in tracks:
        res = download_mp3(track, download_dir)
        results.append(res.json)

    return jsonify({
        "success": True,
        "results": results
    })
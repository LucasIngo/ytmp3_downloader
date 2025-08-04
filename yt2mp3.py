import os
import re
import logging
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from yt_dlp import YoutubeDL

DOWNLOAD_DIR = "downloads"

def sanitize_filename(name: str) -> str:
    """Remove invalid characters from filenames."""
    return re.sub(r'[\\/*?:"<>|]', "", name)

def get_user_input(prompt: str, default: str) -> str:
    """Prompt the user for input and return the result or a default value."""
    user_input = input(f"{prompt} (Enter = {default}): ").strip()
    return user_input if user_input else default

def download_song():
    """Download a YouTube video as MP3 and set metadata."""
    video_url = input("🎥 YouTube-Link eingeben: ").strip()
    if not video_url:
        logging.error("❌ Kein gültiger YouTube-Link eingegeben.")
        return
    
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # 1. Get video info
    ydl_opts_info = {
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
    }
    try:
        with YoutubeDL(ydl_opts_info) as ydl_info:
            info = ydl_info.extract_info(video_url, download=False)
            original_title = info.get("title", "Unbekannter Titel")
            original_artist = info.get("uploader", "Unbekannter Künstler")
    except Exception as e:
        logging.error(f"❌ Fehler beim Abrufen der Video-Infos: {e}")
        return

    logging.info(f"\n📋 Gefundene Informationen:")
    logging.info(f"Titel:   {original_title}")
    logging.info(f"Interpret: {original_artist}")

    title = get_user_input("❓ Neuen Titel eingeben", original_title)
    artist = get_user_input("❓ Neuen Interpreten eingeben", original_artist)

    safe_artist = sanitize_filename(artist)
    safe_title = sanitize_filename(title)
    filename = f"{safe_artist} - {safe_title}.mp3"
    output_path = os.path.join(DOWNLOAD_DIR, filename)

    # 2. Download mit angepasstem Dateinamen (neues Objekt)
    ydl_opts_download = {
        "format": "bestaudio/best",
        "outtmpl": output_path.replace(".mp3", ".%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "0",
        },
        {
            "key": "FFmpegMetadata"
        }],
        "noplaylist": True,
        "quiet": True,
    }
    try:
        with YoutubeDL(ydl_opts_download) as ydl_download:
            print(f"\n📥 Starte Download als: {artist} - {title}.mp3\n")
            ydl_download.download([video_url])
    except Exception as e:
        logging.error(f"❌ Fehler beim Download: {e}")
        return
    update_tags(output_path, artist, title)
    print("✅ Download abgeschlossen.\n")

def update_tags(directory: str,artist: str, title: str) -> None:
    """Update MP3 metadata tags."""
    logging.info("== MP3 Metadaten-Schreiber läuft ==")
    try:
        audio = MP3(directory, ID3 = EasyID3)
        audio['artist'] = artist.strip()
        audio['title'] = title.strip()
        audio.save()
        logging.info(f"[✓] Metadaten gesetzt für '{os.path.basename(directory)}'")
    except Exception as e:
        logging.error(f"❌ Fehler bei Metadaten für '{directory}': {e}")

if __name__ == "__main__":
    while True:
        download_song()
        answer = input("🔄 Möchtest du noch ein Lied herunterladen? (j/n): ").strip().lower()
        if answer != "j":            
            print("👋 Programm beendet.")
            break

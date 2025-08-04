import os
import re
import yaml
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from yt_dlp import YoutubeDL

DOWNLOAD_DIR = "downloads"

def load_config(config_path: str = "config.yml") -> dict:
    """Load configuration from a YAML file."""
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return yaml.safe_load(f) or {}
    return{}
    
def sanitize_filename(name: str) -> str:
    """Remove invalid characters from filenames."""
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_song(config: dict) -> None:
    """Download a YouTube video as MP3 and set metadata."""
    video_url = input("🎥 YouTube-Link eingeben: ").strip()
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
        print(f"❌ Fehler beim Abrufen der Video-Infos: {e}")
        return

    print(f"\n📋 Gefundene Informationen:")
    print(f"Titel:   {original_title}")
    print(f"Interpret: {original_artist}")

    new_title = input(f"❓ Neuen Titel eingeben (Enter = {original_title}): ").strip()
    new_artist = input(f"❓ Neuen Interpreten eingeben (Enter = {original_artist}): ").strip()

    title = new_title if new_title else original_title
    artist = new_artist if new_artist else original_artist

    safe_artist = sanitize_filename(artist)
    safe_title = sanitize_filename(title)
    filename = f"{safe_artist} - {safe_title}.mp3"
    output_path = os.path.join(DOWNLOAD_DIR, filename)

    ydl_opts_download = dict(config)  # copy config
    ydl_opts_download.update({
        "outtmpl": output_path.replace(".mp3", ".%(ext)s"),
        "noplaylist": True,
        "quiet": True,
    })
    try:
        with YoutubeDL(ydl_opts_download) as ydl_download:
            print(f"\n📥 Starte Download als: {filename}\n")
            ydl_download.download([video_url])
    except Exception as e:
        print(f"❌ Fehler beim Download: {e}")
        return

    update_tags(output_path, artist, title)
    print("✅ Download abgeschlossen.\n")

def update_tags(directory: str,artist: str, title: str):
    """Set MP3 metadata tags."""
    print("== MP3 Metadaten-Schreiber läuft ==")
    try:
        audio = MP3(directory, ID3 = EasyID3)
        audio['artist'] = artist.strip()
        audio['title'] = title.strip()
        audio.save()
        print(f"[✓] Metadaten gesetzt für '{os.path.basename(directory)}'")
    except Exception as e:
        print(f"❌ Fehler bei Metadaten für '{directory}': {e}")

if __name__ == "__main__":
    config = load_config()
    while True:
        download_song(config)
        answer = input("🔄 Möchtest du noch ein Lied herunterladen? (j/n): ").strip().lower()
        if answer != "j":            
            print("👋 Programm beendet.")
            break

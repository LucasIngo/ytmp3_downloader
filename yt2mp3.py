import os
import re
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from yt_dlp import YoutubeDL

def download_song():
    video_url = input("🎥 YouTube-Link eingeben: ").strip()
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    # 1. Video-Info holen (extra Objekt)
    ydl_opts_info = {
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
    }
    with YoutubeDL(ydl_opts_info) as ydl_info:
        info = ydl_info.extract_info(video_url, download=False)
        original_title = info.get("title", "Unbekannter Titel")
        original_artist = info.get("uploader", "Unbekannter Künstler")

    print(f"\n📋 Gefundene Informationen:")
    print(f"Titel:   {original_title}")
    print(f"Interpret: {original_artist}")

    new_title = input(f"❓ Neuen Titel eingeben (Enter = {original_title}): ").strip()
    new_artist = input(f"❓ Neuen Interpreten eingeben (Enter = {original_artist}): ").strip()

    title = new_title if new_title else original_title
    artist = new_artist if new_artist else original_artist

    safe_title = "".join(c for c in title if c.isalnum() or c in " -_").strip()
    safe_artist = "".join(c for c in artist if c.isalnum() or c in " -_").strip()

    filename_template = os.path.join(output_dir, f"{safe_artist} - {safe_title}.%(ext)s")

    # 2. Download mit angepasstem Dateinamen (neues Objekt)
    ydl_opts_download = {
        "format": "bestaudio/best",
        "outtmpl": filename_template,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "noplaylist": True,
        "quiet": False,
    }

    with YoutubeDL(ydl_opts_download) as ydl_download:
        print(f"\n📥 Starte Download als: {safe_artist} - {safe_title}.mp3\n")
        ydl_download.download([video_url])

    print("✅ Download abgeschlossen.\n")

def update_tags(directory):
    print("== MP3 Metadaten-Schreiber läuft ==")
    for filename in os.listdir(directory):
        if filename.lower().endswith(".mp3"):
            filepath = os.path.join(directory, filename)

            match = re.match(r"^(.*?) - (.*?)\.mp3$", filename)
            if not match:
                print(f"[!] Überspringe: {filename} (kein passendes Format)")
                continue

            artist, title = match.groups()
            try:
                audio = MP3(filepath, ID3 = EasyID3)
                audio['artist'] = artist.strip()
                audio['title'] = title.strip()
                audio.save()
                print(f"[✓] {filename} → Artist: '{artist}', Title: '{title}'")
            except Exception as e:
                print(f"[!] Fehler bei '{filename}': {e}")

if __name__ == "__main__":
    while True:
        download_song()
        answer = input("🔄 Möchtest du noch ein Lied herunterladen? (j/n): ").strip().lower()
        if answer != "j":
            
            update_tags("downloads/")
            print("👋 Programm beendet.")
            break

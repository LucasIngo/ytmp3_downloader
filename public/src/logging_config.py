import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL,
    format="[%(levelname)s] %(message)s"
)

# yt-dlp extrem ruhig stellen
logging.getLogger("yt_dlp").setLevel(logging.ERROR)

# ffmpeg komplett stummschalten
logging.getLogger("ffmpeg").setLevel(logging.ERROR)

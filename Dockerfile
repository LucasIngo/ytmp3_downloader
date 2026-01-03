FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY public/src/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --upgrade --no-cache-dir yt-dlp

# Copy your app code and public files
COPY public/ ./public/

EXPOSE 5000

WORKDIR /app/public/src

CMD ["python", "yt2mp3.py"]
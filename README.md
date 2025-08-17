# 🎵 ytmp3-downloader (Minimal Web App)

Ein einfaches Python-Webtool, das YouTube-Videos als MP3 herunterlädt und dir vor dem Download erlaubt, Titel und Interpret anzupassen.  
Die Songs werden im Ordner `downloads` gespeichert und können direkt im Browser heruntergeladen werden.

---

## 🚀 Nutzung

1. **Starte das Tool:**
   ```bash
   python yt2mp3.py
   ```
2. **Öffne deinen Browser und gehe zu**  
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

3. **Workflow im Browser:**
   - Gib einen YouTube-Link ein.
   - Klicke auf **Vorschlag holen**.
   - Die Felder für Titel und Interpret erscheinen und werden automatisch ausgefüllt.
   - Passe Titel und Interpret nach Wunsch an.
   - Klicke auf **Download starten**.
   - Nach Abschluss erscheint ein Download-Link zum MP3.

---

## 🗂 Ordnerstruktur

- `public/` – Enthält die Weboberfläche (HTML, CSS, JS)
- `downloads/` – Hier werden die MP3-Dateien gespeichert

---

## ⚙️ Voraussetzungen

- Python 3.8+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [mutagen](https://mutagen.readthedocs.io/en/latest/)
- Flask

Installiere die Abhängigkeiten mit:

```bash
pip install flask yt-dlp mutagen
```

---

## 💡 Hinweise

- Die Metadaten (Titel & Interpret) werden automatisch gesetzt.
- Die Weboberfläche ist minimal gehalten und funktioniert auch auf mobilen Geräten.
- Die MP3-Dateien können direkt nach dem Download im Browser heruntergeladen werden.

---

## 🖥️ Beispielablauf

1. YouTube-Link eingeben und Vorschlag holen:
2. Titel/Interpret anpassen (optional).
3. Download starten und MP3 herunterladen.

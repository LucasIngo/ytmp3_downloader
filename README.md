# 🎵 ytmp3-downloader (Minimal)

Ein einfaches Python-Skript, das YouTube-Videos als MP3 herunterlädt und dir vor dem Download erlaubt, Titel und Interpret anzupassen.
Es wird hierfür ein downloads ordner erstellt, wo die songs gespeichert werden.

---

## 📋 Beispiel: Titel und Interpret vor dem Download anpassen

Das Skript liest zuerst die Video-Infos aus und zeigt dir den gefundenen Titel und Künstler an. Du kannst beide Eingaben anpassen oder einfach mit Enter übernehmen.
Anschließend kann man ein weiteres Lied herunterladen oder alternativ beenden. Das Beenden startet ebenfalls den Metadaten-Schreiber, welcher basierend auf der
Benennung der Datei (Interpret - Titel) diese Daten in die Metadaten einträgt.

### Tool starten:

```bash
python yt2mp3.py
```

### Beispielausgabe im Terminal:

```bash
🎥 YouTube-Link eingeben: https://www.youtube.com/watch?v=dQw4w9WgXcQ

📋 Gefundene Informationen:
Titel:   Rick Astley - Never Gonna Give You Up (Official Music Video)
Interpret: Rick Astley

❓ Neuen Titel eingeben (Enter = Rick Astley - Never Gonna Give You Up (Official Music Video)): Never Gonna Give You Up
❓ Neuen Interpreten eingeben (Enter = Rick Astley): Rick Astley

📥 Starte Download als: Rick Astley - Never Gonna Give You Up.mp3

✅ Download abgeschlossen.

 Möchtest du noch ein Lied herunterladen? (j/n):
```

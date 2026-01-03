const status = document.getElementById("status");
const suggestBtn = document.getElementById("suggest");
const downloadBtn = document.getElementById("download");
const spinner = document.getElementById("spinner");
const metaFields = document.getElementById("meta-fields");
const playlistTable = document.getElementById("playlist-table");
const playlistBody = playlistTable.querySelector("tbody");
let playlistTracks = [];

function showSpinner(show) {
  spinner.style.display = show ? "inline-block" : "none";
}

suggestBtn.addEventListener("click", async (e) => {
  e.preventDefault();
  suggestBtn.disabled = true;
  showSpinner(true);
  status.textContent = "Hole Vorschlag...";
  const url = document.getElementById("url").value;
  if (!url.startsWith("http")) {
    status.textContent = "Bitte gib eine gültige URL ein.";
    return;
  }

  try {
    const res = await fetch("/suggest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });
    if (!res.ok) throw new Error("Serverfehler");
    const data = await res.json();
    if (data.success) {
      playlistTracks = data.tracks;

      // Einzelvideo
      if (data.type === "single") {
        document.getElementById("title").value = playlistTracks[0].title;
        document.getElementById("artist").value = playlistTracks[0].artist;
        metaFields.style.display = "block";
        playlistTable.style.display = "none";
      }

      // Playlist
      else {
        playlistBody.innerHTML = "";
        playlistTracks.forEach((track, i) => {
          const row = document.createElement("tr");
          row.innerHTML = `
        <td>${i + 1}</td>
        <td><input value="${track.title}"></td>
        <td><input value="${track.artist}"></td>
      `;
          playlistBody.appendChild(row);
        });

        playlistTable.style.display = "table";
        metaFields.style.display = "none";
      }

      downloadBtn.disabled = false;
    }
  } catch (err) {
    status.textContent = "Netzwerkfehler!";
    metaFields.style.display = "none";
    status.style.color = "#c62828";
  }
  suggestBtn.disabled = false;
  showSpinner(false);
});

downloadBtn.addEventListener("click", async (e) => {
  e.preventDefault();

  downloadBtn.disabled = true;
  showSpinner(true);
  status.textContent = "Download läuft...";
  status.style.color = "#1565c0";

  // Playlist
  if (playlistTable.style.display === "table") {
    const rows = playlistBody.querySelectorAll("tr");

    rows.forEach((row, i) => {
      playlistTracks[i].title = row.children[1].querySelector("input").value;
      playlistTracks[i].artist = row.children[2].querySelector("input").value;
    });

    await fetch("/download-playlist", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tracks: playlistTracks }),
    });
    showSpinner(false);
    status.textContent = "✅ Playlist Download abgeschlossen";
    return;
  }

  // Einzelvideo
  const payload = {
    url: document.getElementById("url").value,
    title: document.getElementById("title").value,
    artist: document.getElementById("artist").value,
  };

  await fetch("/download", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  showSpinner(false);
  status.textContent = "✅ Download abgeschlossen";
});

function resizeUrlInput(input) {
  // Calculate width based on value length, but keep min/max
  const minWidth = 350;
  const maxWidth = window.innerWidth * 0.9;
  const tempSpan = document.createElement("span");
  tempSpan.style.visibility = "hidden";
  tempSpan.style.position = "fixed";
  tempSpan.style.font = globalThis.getComputedStyle(input).font;
  tempSpan.textContent = input.value || input.placeholder;
  document.body.appendChild(tempSpan);
  let newWidth = tempSpan.offsetWidth + 30;
  tempSpan.remove();
  if (newWidth < minWidth) newWidth = minWidth;
  if (newWidth > maxWidth) newWidth = maxWidth;
  input.style.width = newWidth + "px";
}

// Set initial width on page load
globalThis.addEventListener("DOMContentLoaded", () => {
  const urlInput = document.getElementById("url");
  resizeUrlInput(urlInput);
});

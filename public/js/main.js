const status = document.getElementById("status");
const suggestBtn = document.getElementById("suggest");
const downloadBtn = document.getElementById("download");
const spinner = document.getElementById("spinner");
const metaFields = document.getElementById("meta-fields");

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
      document.getElementById("title").value = data.title;
      document.getElementById("artist").value = data.artist;
      status.textContent =
        "Vorschlag geladen. Du kannst Titel/Interpret ändern.";
      downloadBtn.disabled = false;
      metaFields.style.display = "block";
      status.style.color = "#2e7d32";
    } else {
      status.textContent = "Fehler: " + data.message;
      metaFields.style.display = "none";
      status.style.color = "#c62828";
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
  const payload = {
    url: document.getElementById("url").value,
    title: document.getElementById("title").value,
    artist: document.getElementById("artist").value,
  };
  try {
    const res = await fetch("/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Serverfehler");
    const data = await res.json();
    if (data.success) {
      status.innerHTML = `✅ Download abgeschlossen: <a href="/downloads/${encodeURIComponent(
        data.filename
      )}" target="_blank">${data.filename}</a>`;
      status.style.color = "#2e7d32";
      document.getElementById("title").value = "";
      document.getElementById("artist").value = "";
      document.getElementById("url").value = "";
      downloadBtn.disabled = true;
      metaFields.style.display = "none";
    } else {
      status.textContent = "Fehler: " + data.message;
      status.style.color = "#c62828";
    }
  } catch (err) {
    status.textContent = "Netzwerkfehler!";
    status.style.color = "#c62828";
  }
  showSpinner(false);
  downloadBtn.disabled = false;
});

function resizeUrlInput(input) {
  // Calculate width based on value length, but keep min/max
  const minWidth = 350;
  const maxWidth = window.innerWidth * 0.9;
  const tempSpan = document.createElement("span");
  tempSpan.style.visibility = "hidden";
  tempSpan.style.position = "fixed";
  tempSpan.style.font = window.getComputedStyle(input).font;
  tempSpan.textContent = input.value || input.placeholder;
  document.body.appendChild(tempSpan);
  let newWidth = tempSpan.offsetWidth + 30;
  tempSpan.remove();
  if (newWidth < minWidth) newWidth = minWidth;
  if (newWidth > maxWidth) newWidth = maxWidth;
  input.style.width = newWidth + "px";
}

// Set initial width on page load
window.addEventListener("DOMContentLoaded", () => {
  const urlInput = document.getElementById("url");
  resizeUrlInput(urlInput);
});

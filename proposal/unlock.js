async function openSharedPage() {
  const encodedKey = location.hash.slice(1);
  if (!encodedKey) return;

  const status = document.getElementById("status");
  if (!/^[A-Za-z0-9_-]{43}$/.test(encodedKey) || !crypto.subtle) {
    status.textContent = "Open the complete HTTPS share link in a current browser.";
    return;
  }

  status.textContent = "Opening the shared page…";
  try {
    const base64Key = encodedKey.replaceAll("-", "+").replaceAll("_", "/") + "=";
    const bytes = Uint8Array.from(atob(base64Key), character => character.charCodeAt(0));
    const key = await crypto.subtle.importKey("raw", bytes, "AES-GCM", false, ["decrypt"]);
    const response = await fetch("content.bin?v=bb4e61f86426f4ec", { credentials: "omit" });
    if (!response.ok) throw new Error("Content unavailable");
    const payload = new Uint8Array(await response.arrayBuffer());
    const documentBytes = await crypto.subtle.decrypt({
      name: "AES-GCM",
      iv: payload.subarray(0, 12),
      additionalData: new TextEncoder().encode("commonroad-proposal-v1"),
    }, key, payload.subarray(12));

    const title = new TextDecoder().decode(documentBytes).match(/<title>([^<]+)<\/title>/i)?.[1];
    const frame = document.createElement("iframe");
    frame.title = title || "Research proposal";
    frame.allowFullscreen = true;
    frame.setAttribute("sandbox", "allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox");
    const url = URL.createObjectURL(new Blob([documentBytes], { type: "text/html;charset=utf-8" }));
    frame.src = url;
    window.addEventListener("pagehide", (event) => {
      if (!event.persisted) URL.revokeObjectURL(url);
    });
    document.getElementById("gate").replaceWith(frame);
    document.title = frame.title;
  } catch {
    status.textContent = "Unable to open this page. Check the complete share link or try again later.";
  }
}

openSharedPage();

const BACKEND_URL =
  import.meta.env.VITE_BACKEND_URL || "http://localhost:8080";

export async function sendChatMessage(message, language = "en") {
  const res = await fetch(`${BACKEND_URL}/api/chat/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      language,
    }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "Backend error");
  }

  return await res.json();
}

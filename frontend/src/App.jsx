import { useState } from "react";
import { sendChatMessage } from "./services/api";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState("en"); // optional, backend already supports it

  const sendMessage = async () => {
    if (!message.trim()) return;

    // Add user message
    const userMsg = { from: "user", text: message };
    setChat(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const data = await sendChatMessage(message, language);

      // Add bot message (IMPORTANT: use data.answer)
      const botMsg = { from: "bot", text: data.answer };
      setChat(prev => [...prev, botMsg]);
    } catch (err) {
      setChat(prev => [
        ...prev,
        { from: "bot", text: "❌ Backend error. Please try again." }
      ]);
    }

    setMessage("");
    setLoading(false);
  };

  return (
    <div style={{ padding: 20, maxWidth: 800, margin: "auto" }}>
      <h1>SahajAI</h1>

      {/* Language Toggle */}
      <div style={{ marginBottom: 10 }}>
        <button onClick={() => setLanguage("en")}>EN</button>
        <button onClick={() => setLanguage("hi")} style={{ marginLeft: 5 }}>
          HI
        </button>
      </div>

      {/* Chat Box */}
      <div
        style={{
          border: "1px solid #ccc",
          padding: 10,
          minHeight: 300,
          borderRadius: 4
        }}
      >
        {chat.map((msg, i) => (
          <div
            key={i}
            style={{
              textAlign: msg.from === "user" ? "right" : "left",
              marginBottom: 8,
              whiteSpace: "pre-line" // ✅ multiline support
            }}
          >
            <b>{msg.from === "user" ? "You" : "SahajAI"}:</b>{" "}
            {msg.text}
          </div>
        ))}

        {loading && <div>SahajAI is typing...</div>}
      </div>

      {/* Input Box */}
      <div style={{ marginTop: 10 }}>
        <input
          style={{ width: "80%", padding: 6 }}
          value={message}
          onChange={e => setMessage(e.target.value)}
          onKeyDown={e => {
            if (e.key === "Enter") sendMessage();
          }}
          placeholder="Ask about government schemes, documents..."
        />
        <button onClick={sendMessage} style={{ marginLeft: 5 }}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;

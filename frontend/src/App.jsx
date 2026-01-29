import { useState } from "react";
import { sendChatMessage } from "./services/api";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMsg = { from: "user", text: message };
    setChat(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const data = await sendChatMessage(message, "en");

      const botMsg = { from: "bot", text: data.reply };
      setChat(prev => [...prev, botMsg]);
    } catch (err) {
      setChat(prev => [...prev, { from: "bot", text: "❌ Backend error" }]);
    }

    setMessage("");
    setLoading(false);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>SahajAI</h1>

      <div style={{ border: "1px solid #ccc", padding: 10, minHeight: 300 }}>
        {chat.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.from === "user" ? "right" : "left" }}>
            <b>{msg.from === "user" ? "You" : "SahajAI"}:</b> {msg.text}
          </div>
        ))}
        {loading && <div>SahajAI is typing...</div>}
      </div>

      <div style={{ marginTop: 10 }}>
        <input
          style={{ width: "80%" }}
          value={message}
          onChange={e => setMessage(e.target.value)}
          placeholder="Ask about government schemes..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;

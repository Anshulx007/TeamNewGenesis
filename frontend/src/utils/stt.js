// Speech to Text utility

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

export function startSpeechRecognition({
  language = "en",
  onResult,
  onError,
  onEnd,
}) {
  if (!SpeechRecognition) {
    alert("Speech recognition not supported in this browser");
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = language === "hi" ? "hi-IN" : "en-IN";
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    onResult && onResult(transcript);
  };

  recognition.onerror = (err) => {
    console.error("Speech recognition error", err);
    onError && onError(err);
  };

  recognition.onend = () => {
    onEnd && onEnd();
  };

  recognition.start();
}

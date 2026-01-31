// Text to Speech utility

export function speakText(text, language = "en") {
  if (!("speechSynthesis" in window)) {
    console.warn("Text-to-speech not supported in this browser");
    return;
  }

  // Stop any ongoing speech
  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = language === "hi" ? "hi-IN" : "en-IN";
  utterance.rate = 1;
  utterance.pitch = 1;

  window.speechSynthesis.speak(utterance);
}

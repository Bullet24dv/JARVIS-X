const ws = new WebSocket("ws://localhost:8000/ws");
const messagesDiv = document.getElementById("messages");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const voiceBtn = document.getElementById("voice-btn");

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === "voice_response") {
        addMessage("JARVIS", data.text);
    }
};

function addMessage(sender, text) {
    const msgDiv = document.createElement("div");
    msgDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
    messagesDiv.appendChild(msgDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

sendBtn.addEventListener("click", () => {
    const text = userInput.value;
    if (text) {
        addMessage("Tú", text);
        ws.send(JSON.stringify({ type: "text_command", data: { text } }));
        userInput.value = "";
    }
});

if ("webkitSpeechRecognition" in window) {
    const recognition = new webkitSpeechRecognition();
    recognition.lang = "es-CL";
    recognition.continuous = false;
    voiceBtn.addEventListener("click", () => {
        recognition.start();
    });
    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        userInput.value = text;
        sendBtn.click();
    };
}
const sendBtn = document.getElementById("send-btn");
const input = document.getElementById("user-input");
const chatWindow = document.getElementById("chat-window");
const fileInput = document.getElementById("file-upload");

function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = `message ${sender}-message`;
    div.textContent = text;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Handle File Upload
fileInput.addEventListener("change", async () => {
    const file = fileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("http://127.0.0.1:8080/upload", {
            method: "POST",
            body: formData
        });

        if (res.ok) {
            const data = await res.json();
            addMessage(`📁 File uploaded: ${file.name}. You can now ask questions about it.`, "bot");
        } else {
            addMessage("⚠️ Failed to upload file.", "bot");
        }
    } catch (err) {
        addMessage("⚠️ Error connecting to backend for file upload.", "bot");
    }
});

sendBtn.addEventListener("click", async () => {
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, "user");
    input.value = "";

    try {
        const res = await fetch("http://127.0.0.1:8080/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await res.json();
        addMessage(data.reply, "bot");

    } catch (err) {
        addMessage("⚠️ Server error. Check backend.", "bot");
    }
});


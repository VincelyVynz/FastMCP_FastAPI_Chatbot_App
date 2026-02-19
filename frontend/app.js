window.addEventListener("beforeunload", () => {
    console.log("REAL PAGE RELOAD");
});


const sendBtn = document.getElementById("send-btn");
const input = document.getElementById("user-input");
const chatWindow = document.getElementById("chat-window");
const fileInput = document.getElementById("file-upload");
const fileLabel = document.querySelector("label[for='file-upload']");

let currentFile = null;
let isLoading = false;

// ============================
// Focus input on page load
// ============================
window.addEventListener("load", () => {
    input.focus();
});

// ============================
// Add message to chat
// ============================
function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = `message ${sender}-message`;
    div.textContent = text;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// ============================
// File Upload Handler
// ============================
fileInput.addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("http://127.0.0.1:8080/upload", {
            method: "POST",
            body: formData
        });

        if (!res.ok) throw new Error("Upload failed");

        const data = await res.json();
        currentFile = data.filename;

        fileLabel.textContent = `RAG File: ${file.name}`;
        addMessage(`📁 File uploaded: ${file.name}. You can now ask questions about it.`, "bot");

        input.focus(); // Refocus after upload

    } catch (err) {
        console.error("Upload error:", err);
        addMessage("⚠️ Error uploading file. Check backend.", "bot");
        input.focus();
    }
});

// ============================
// Send Message
// ============================
async function sendMessage() {
    if (isLoading) return; // Prevent spam clicks

    const message = input.value.trim();
    if (!message) return;

    isLoading = true;
    sendBtn.disabled = true;

    addMessage(message, "user");
    input.value = "";

    try {
        const res = await fetch("http://127.0.0.1:8080/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: message,
                filename: currentFile
            })
        });

        if (!res.ok) throw new Error("Chat request failed");

        const data = await res.json();
        addMessage(data.reply || "⚠️ No response from server.", "bot");

    } catch (err) {
        console.error("Chat error:", err);
        addMessage("⚠️ Server error. Check backend.", "bot");
    }

    isLoading = false;
    sendBtn.disabled = false;
    input.focus(); // Refocus after sending
}

// ============================
// Button Click
// ============================
sendBtn.addEventListener("click", sendMessage);

// ============================
// Enter Key = Send
// ============================
input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault(); // Prevent newline
        sendMessage();
    }
});

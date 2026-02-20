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
// File Selection Handler
// ============================
fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (!file) {
        currentFile = null;
        fileLabel.textContent = "RAG Files:";
        return;
    }

    currentFile = file.name; // Just store the name

    fileLabel.textContent = `RAG File: ${file.name}`;
    addMessage(`📁 File selected: ${file.name}. The file will be sent with your next message.`, "bot");

    input.focus();
});


// ============================
// Send Message
// ============================
async function sendMessage() {
    if (isLoading) return; // Prevent spam clicks

    const message = input.value.trim();
    if (!message && !currentFile) return;

    isLoading = true;
    sendBtn.disabled = true;

    addMessage(message, "user");
    input.value = "";

    try {
        const res = await fetch("http://127.0.0.1:8000/chat", {
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

    // Clear the file after sending
    currentFile = null;
    fileInput.value = ""; // Reset the file input
    fileLabel.textContent = "RAG Files:";


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

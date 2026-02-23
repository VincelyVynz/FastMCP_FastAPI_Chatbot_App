document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const fileUpload = document.getElementById('file-upload');
    const selectedFileName = document.getElementById('selected-file-name');
    const unchooseFileBtn = document.getElementById('unchoose-file');

    let selectedFile = null;

    // Handle file selection
    fileUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            selectedFile = file;
            selectedFileName.textContent = file.name;
            unchooseFileBtn.style.display = 'inline-block';
        }
    });

    // Handle unchoose file
    unchooseFileBtn.addEventListener('click', () => {
        selectedFile = null;
        fileUpload.value = ''; // Reset file input
        selectedFileName.textContent = 'No file chosen';
        unchooseFileBtn.style.display = 'none';
    });

    // Handle sending message
    const sendMessage = async () => {
        const message = userInput.value.trim();
        if (!message) return;

        // Display user message
        appendMessage('user', message);
        userInput.value = '';

        try {
            const formData = new FormData();
            formData.append('message', message);
            if (selectedFile) {
                formData.append('file', selectedFile);
            }

            const response = await fetch('/chat', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            appendMessage('bot', data.reply);
        } catch (error) {
            console.error('Error:', error);
            appendMessage('bot', 'Sorry, something went wrong.');
        }
    };

    const appendMessage = (role, text) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(role === 'user' ? 'user-message' : 'bot-message');
        messageDiv.textContent = text;
        chatWindow.appendChild(messageDiv);

        // Scroll to bottom
        const chatContainer = document.getElementById('chat-container');
        chatContainer.scrollTop = chatContainer.scrollHeight;
    };

    sendBtn.addEventListener('click', sendMessage);

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});


const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const resetButton = document.getElementById("reset-button");


/*
 Add a message to the chat window.
*/

function addMessage(message, sender) {

    const messageElement = document.createElement("div");

    messageElement.classList.add(
        sender === "bot" ? "bot-message" : "user-message"
    );

    messageElement.textContent = message;

    chatBox.appendChild(messageElement);

    chatBox.scrollTop = chatBox.scrollHeight;
}


/*
 Handle customer messages.
*/

chatForm.addEventListener("submit", async (event) => {

    event.preventDefault();

    const message = userInput.value.trim();

    if (!message) return;

    // Display customer message
    addMessage(message, "user");

    userInput.value = "";

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        // Display chatbot response
        addMessage(data.response, "bot");

    } catch (error) {

        addMessage(error.message, "bot");

    }

});


/*
 Restart the conversation.
*/

resetButton.addEventListener("click", async () => {

    try {

        const response = await fetch("/reset", {
            method: "POST"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to restart.");
        }

        chatBox.innerHTML = "";

        addMessage(data.response, "bot");

    } catch (error) {

        addMessage(error.message, "bot");

    }

});

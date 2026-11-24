
const chatBox = document.getElementById("chat-box");
const choiceContainer = document.getElementById("choice-container");
const resetButton = document.getElementById("reset-button");


function addMessage(message, sender) {
    const messageElement = document.createElement("div");

    messageElement.classList.add(
        sender === "bot" ? "bot-message" : "user-message"
    );

    messageElement.textContent = message;

    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}


function displayChoices(state) {
    choiceContainer.innerHTML = "";

    let options = [];

    if (state === "order") {
        options = [
            { label: "☕ Latte - AED 18", value: "latte" },
            { label: "☕ Cappuccino - AED 16", value: "cappuccino" },
            { label: "☕ Espresso - AED 10", value: "espresso" }
        ];
    }

    if (state === "confirmation") {
        options = [
            { label: "Confirm Order", value: "yes" },
            { label: "Cancel Order", value: "cancel" }
        ];
    }

    options.forEach(option => {
        const button = document.createElement("button");

        button.textContent = option.label;
        button.classList.add("choice-button");

        button.addEventListener("click", () => {
            sendMessage(option.value, option.label);
        });

        choiceContainer.appendChild(button);
    });
}


async function sendMessage(message, displayText = message) {
    addMessage(displayText, "user");

    choiceContainer.innerHTML = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        addMessage(data.response, "bot");

        displayChoices(data.current_state);

    } catch (error) {
        addMessage(error.message, "bot");
    }
}


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
        displayChoices(data.current_state);

    } catch (error) {
        addMessage(error.message, "bot");
    }
});


// Display the initial coffee options.
displayChoices("order");


from pathlib import Path

from flask import Flask, render_template, request, jsonify, session

from chatbot.decision_engine import DecisionEngine


# Project paths
BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config" / "sales_tree.json"


# Initialize Flask
app = Flask(__name__)

app.secret_key = "coffee-bot-development-secret"


# Initialize decision engine
bot = DecisionEngine(CONFIG_PATH)


@app.route("/")
def home():
    """Display the chatbot interface."""

    session["current_state"] = "order"
    session["order_context"] = {}

    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """Process a customer message."""

    data = request.get_json(silent=True) or {}

    user_input = data.get("message", "")

    if not isinstance(user_input, str) or not user_input.strip():
        return jsonify({
            "error": "Please enter a message."
        }), 400

    current_state = session.get(
        "current_state",
        bot.start_state
    )

    context = session.get("order_context", {})

    result = bot.process_message(
        user_input,
        current_state,
        context
    )

    session["current_state"] = result["next_state"]
    session["order_context"] = result["context"]

    return jsonify({
        "response": result["response"],
        "current_state": result["next_state"],
        "matched": result["matched"]
    })


@app.route("/reset", methods=["POST"])
def reset():
    """Reset the conversation."""

    session["current_state"] = "order"
    session["order_context"] = {}

    return jsonify({
        "response": "Hello! Welcome to our coffee shop. What would you like to order?",
        "current_state": "order"
    })


if __name__ == "__main__":
    app.run(debug=True)

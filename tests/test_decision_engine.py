
import pytest
from pathlib import Path

from chatbot.decision_engine import DecisionEngine


# Locate the project root and JSON configuration file
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "sales_tree.json"


@pytest.fixture
def bot():
    """Create a fresh decision engine for each test."""
    return DecisionEngine(CONFIG_PATH)


def test_greeting_with_hi(bot):
    result = bot.process_message("hi", "greeting")

    assert result["matched"] is True
    assert result["next_state"] == "order"
    assert "Welcome to our coffee shop" in result["response"]


@pytest.mark.parametrize("message", ["hello", "hey"])
def test_other_greeting_keywords(bot, message):
    result = bot.process_message(message, "greeting")

    assert result["matched"] is True
    assert result["next_state"] == "order"


def test_menu_keyword(bot):
    result = bot.process_message("show me the menu", "greeting")

    assert result["matched"] is True
    assert result["next_state"] == "order"
    assert "Latte" in result["response"]


@pytest.mark.parametrize(
    ("coffee", "expected_item", "expected_price"),
    [
        ("latte", "Latte", "AED 18"),
        ("cappuccino", "Cappuccino", "AED 16"),
        ("espresso", "Espresso", "AED 10"),
    ],
)
def test_coffee_selection(bot, coffee, expected_item, expected_price):
    result = bot.process_message(coffee, "order")

    assert result["matched"] is True
    assert result["next_state"] == "confirmation"
    assert result["context"]["item"] == expected_item
    assert result["context"]["price"] == expected_price


def test_invalid_coffee_selection(bot):
    result = bot.process_message("tea", "order")

    assert result["matched"] is False
    assert result["next_state"] == "order"
    assert "Please choose one of our coffees" in result["response"]


def test_successful_order_confirmation(bot):
    # First, select a Latte
    selection = bot.process_message("latte", "order")

    # Then, confirm the order
    result = bot.process_message(
        "yes",
        selection["next_state"],
        selection["context"]
    )

    assert result["matched"] is True
    assert result["next_state"] == "greeting"
    assert result["response"] == (
        "Your Latte (AED 18) is confirmed! "
        "Thank you for ordering with us."
    )
    assert result["context"] == {}


def test_order_cancellation(bot):
    # First, select a Cappuccino
    selection = bot.process_message("cappuccino", "order")

    # Then, cancel the order
    result = bot.process_message(
        "cancel",
        selection["next_state"],
        selection["context"]
    )

    assert result["matched"] is True
    assert result["next_state"] == "greeting"
    assert "order has been cancelled" in result["response"]
    assert result["context"] == {}


def test_invalid_confirmation_keeps_order_context(bot):
    # Select Espresso
    selection = bot.process_message("espresso", "order")

    # Enter an invalid confirmation response
    result = bot.process_message(
        "maybe",
        selection["next_state"],
        selection["context"]
    )

    assert result["matched"] is False
    assert result["next_state"] == "confirmation"
    assert result["context"]["item"] == "Espresso"
    assert result["context"]["price"] == "AED 10"
    assert "Espresso order" in result["response"]


def test_confirmation_with_ok_keyword(bot):
    selection = bot.process_message("latte", "order")

    result = bot.process_message(
        "ok",
        selection["next_state"],
        selection["context"]
    )

    assert result["matched"] is True
    assert result["next_state"] == "greeting"
    assert result["context"] == {}


def test_each_state_has_maximum_three_conditions(bot):
    for state_name, state in bot.states.items():
        assert len(state["conditions"]) <= 3, (
            f"State '{state_name}' exceeds three conditions"
        )


from chatbot.decision_engine import DecisionEngine


bot = DecisionEngine("config/sales_tree.json")

state = bot.start_state
context = {}

while True:

    user_input = input("Customer: ")

    result = bot.process_message(
        user_input,
        state,
        context
    )

    print("Bot:", result["response"])

    state = result["next_state"]
    context = result["context"]

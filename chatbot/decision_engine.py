
import json

from chatbot.text_matcher import match_keyword


class DecisionEngine:

    def __init__(self, config_path):

        with open(config_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)

        self.states = self.config["states"]
        self.start_state = self.config["start_state"]

        self.validate_config()

    def validate_config(self):

        if self.start_state not in self.states:
            raise ValueError("Invalid start state")

        for state_name, state in self.states.items():

            conditions = state["conditions"]

            if len(conditions) > 3:
                raise ValueError(
                    f"State '{state_name}' exceeds 3 conditions"
                )

            for condition in conditions:

                next_state = condition["next_state"]

                if next_state is not None and next_state not in self.states:
                    raise ValueError(
                        f"Invalid next state '{next_state}'"
                    )

    def process_message(self, user_input, current_state, context=None):

        if context is None:
            context = {}

        if current_state not in self.states:
            current_state = self.start_state

        state = self.states[current_state]

        for condition in state["conditions"]:

            if match_keyword(user_input, condition["keywords"]):

                # Save customer selections
                saved_values = condition.get("save", {})
                context.update(saved_values)

                # Generate the predefined response
                response = condition["response"].format(**context)

                # Clear order details when confirmed or cancelled
                if condition.get("clear_context", False):
                    context = {}

                return {
                    "response": response,
                    "next_state": condition["next_state"],
                    "matched": True,
                    "context": context
                }

        # No condition matched
        fallback = state["fallback"].format(**context)

        return {
            "response": fallback,
            "next_state": current_state,
            "matched": False,
            "context": context
        }

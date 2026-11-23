
import re


def match_keyword(user_input, keywords):
    """
    Check whether user input contains any configured keyword.
    Uses whole-word matching to avoid partial matches.
    """

    normalized_input = user_input.lower().strip()

    for keyword in keywords:
        keyword = keyword.lower().strip()

        pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"

        if re.search(pattern, normalized_input):
            return True

    return False

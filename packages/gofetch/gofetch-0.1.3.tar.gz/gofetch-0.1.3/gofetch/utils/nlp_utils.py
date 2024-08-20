"Natural Language Processing module"

import re


def strip_text(text: str) -> str:
    """
    Strips and cleans up text.

    @params:
    - text (str):
        The text to strip and clean up.

    @returns:
    - str:
        The cleaned-up text.
    """
    if not isinstance(text, str):
        return ""
    text = text.strip()
    return re.sub(r"\s+", " ", text)

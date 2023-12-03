"""Service for handling everything related to token calculations."""

def calculate_tokens(text: str) -> int:
    """Calculate the number of tokens in a string of text."""
    # TODO This is a very naive implementation.
    return len(text.split(" "))
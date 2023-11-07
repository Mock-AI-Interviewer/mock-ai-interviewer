def clean_sentance(sentance: str) -> str:
    """Cleans up sentances"""
    return sentance.strip()

def speak_sentance(sentance: str) -> None:
    """Speaks a sentance"""
    print(f"Interviewer Speaking: {sentance}")
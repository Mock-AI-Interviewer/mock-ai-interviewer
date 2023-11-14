def clean_sentance(sentance: str) -> str:
    """Cleans up sentances"""
    return sentance.strip()

def speak_sentance(sentance: str) -> bytes:
    """Returns bytes for the audio for a sentance"""
    raise NotImplementedError("TTSClient.speak_sentance is not yet implemented.")

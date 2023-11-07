from abc import ABC, abstractmethod


class TextToSpeech(ABC):
    @abstractmethod
    def __init__(self):
        pass
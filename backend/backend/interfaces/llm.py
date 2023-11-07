from abc import ABC, abstractmethod


class LLM(ABC):
    @abstractmethod
    def __init__(self):
        pass

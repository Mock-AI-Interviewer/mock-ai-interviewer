from dataclasses import dataclass
from enum import Enum


@dataclass
class SentenceResponse:
    text: str
    timestamp: str
    finish_reason: str


class ResponseFormat(Enum):
    TEXT = "text"
    JSON = "json"

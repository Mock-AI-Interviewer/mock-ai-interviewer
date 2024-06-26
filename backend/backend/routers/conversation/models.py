import asyncio
import json
import logging
from base64 import b64encode
from enum import Enum
from typing import Union

from fastapi import WebSocket
from pydantic import BaseModel

from backend.constants import STOP_MESSAGE_PATTERN

LOGGER = logging.getLogger(__name__)
ASYNCIO_PAUSE_TIME = 0.1


class RecievedStopMessageException(Exception):
    pass


class MessageType(Enum):
    AUDIO = "audio"
    TEXT = "text"
    STOP = STOP_MESSAGE_PATTERN


class Message(BaseModel):
    type: MessageType
    data: Union[str, bytes]


class CandidateMessage(Message):
    pass


class InterviewerMessage(Message):
    pass


async def send_message(
    websocket: WebSocket,
    message: InterviewerMessage,
    asyncio_pause_time: float = ASYNCIO_PAUSE_TIME,
) -> None:
    json_string = message.json()
    await websocket.send_text(json_string)
    await asyncio.sleep(
        asyncio_pause_time
    )  # TODO #37 This is a temporary solution to allow event loop a chance to send data


def is_stop_message(candidate_message: CandidateMessage) -> bool:
    """
    Checks if the given data is a stop message based on the type of the message.
    """
    return candidate_message.type == MessageType.STOP


def encode_to_base64(binary_data):
    return b64encode(binary_data).decode("utf-8")

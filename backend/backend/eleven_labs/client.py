import logging

from elevenlabs import generate, play, set_api_key, stream
from fastapi import APIRouter, FastAPI, Request, WebSocket

from backend.routers.conversation.models import (
    InterviewerMessage,
    MessageType,
    send_message,
    encode_to_base64
)

LOGGER = logging.getLogger(__name__)
CHUNK_SIZE = 4000


def clean_sentence(sentance: str) -> str:
    """Cleans up sentances"""
    return sentance.strip()


async def speak_sentence(websocket: WebSocket, sentence: str) -> InterviewerMessage:
    """Returns bytes for the audio for a sentence"""
    sentence = clean_sentence(sentence)
    for audio_chunk in generate(
        text=sentence,
        stream_chunk_size=CHUNK_SIZE,
        stream=True,
        latency=1,
    ):
        encoded_audio = encode_to_base64(audio_chunk)
        await send_message(
            websocket, InterviewerMessage(type=MessageType.AUDIO, data=encoded_audio)
        )

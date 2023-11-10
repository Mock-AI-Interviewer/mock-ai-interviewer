import asyncio
import io
import logging
import os

import aiofiles
from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.conf import get_root_package_path, initialise_app, get_jinja_templates_path
from fastapi import WebSocket, Query
from typing import Union
from backend.constants import STOP_MESSAGE_PATTERN


async def handle_audio_stream(websocket: WebSocket, user_id: str):
    """
    Handles incoming audio stream until a stop message is received.
    """
    while True:
        audio_data = await websocket.receive_bytes()
        if is_stop_message(audio_data):  # Define how to recognize a stop message
            break
        await handle_audio_input(user_id, audio_data)


async def handle_audio_input(user_id: str, audio_data: bytes):
    """
    Handles incoming audio data.
    """
    pass


async def handle_text_stream(websocket: WebSocket, user_id: str):
    """
    Handles incoming text stream until a stop message is received.
    TODO move to stream handlers
    """
    while True:
        text_data = await websocket.receive_text()
        if is_stop_message(text_data):
            break
        await handle_text_input(user_id, text_data)


async def handle_text_input(user_id: str, text_data: str):
    """
    Handles incoming text data.
    """
    pass


def is_stop_message(data: Union[str, bytes]) -> bool:
    """
    Checks if the given data is a stop message based on the configured stop message pattern.
    """

    if isinstance(data, bytes):
        try:
            return data.decode("utf-8") == STOP_MESSAGE_PATTERN
        except UnicodeDecodeError:
            return False
    elif isinstance(data, str):
        return data == STOP_MESSAGE_PATTERN

    return False

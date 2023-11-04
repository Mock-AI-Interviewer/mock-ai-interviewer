from fastapi import APIRouter, WebSocket
from .speech_client import client
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
websocket_routes = APIRouter()

@websocket_routes.websocket("/ws/audio")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            LOGGER.info(f"Received audio chunk of size: {len(data)}")
            # Process your audio data here
            await asyncio.sleep(1)
            # For example, you can send it back to the client
            await websocket.send_bytes(data)
    except Exception as e:
        LOGGER.info(f"Error: {str(e)}")
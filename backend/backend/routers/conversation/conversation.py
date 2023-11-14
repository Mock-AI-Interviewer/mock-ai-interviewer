import logging

from fastapi import APIRouter, Query, Request, WebSocket, WebSocketDisconnect

from backend.common import get_jinja_templates
from backend.constants import STOP_MESSAGE_PATTERN
from backend.conf import get_root_package_path
from backend.routers.conversation.output_handlers import generate_response
from backend.routers.conversation.stream_handlers import (
    handle_audio_stream,
    handle_text_stream,
)

LOGGER = logging.getLogger(__name__)
ROUTER_PREFIX = "/conversation"
WEBSOCKET_PREFIX = "/response"
TEMPLATE_NAME = "conversation.html"
AUDIO_FILES_DIRECTORY = get_root_package_path()

router = APIRouter(
    prefix=ROUTER_PREFIX,
    responses={},
)


@router.websocket(WEBSOCKET_PREFIX)
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str = Query(...),
    enable_audio_input: bool = Query(False),
    enable_audio_output: bool = Query(False),
):
    """
    Handles a WebSocket connection for audio and text data, processing the data accordingly.
    - If enable_audio_input is True, incoming audio data is processed, followed by generating a response.
    - If enable_audio_input is False, incoming text data is processed, followed by generating a response.
    - The generated response depends on the enable_audio_output flag.
    """
    await websocket.accept()
    
    try:
        while True:
            await generate_response(
                websocket=websocket,
                enable_audio_output=enable_audio_output
            )
            
            if enable_audio_input:
                await handle_audio_stream(websocket, user_id)
            else:
                await handle_text_stream(websocket, user_id)

            
    except WebSocketDisconnect:
        LOGGER.info(f"User {user_id} disconnected.")


@router.get("/")
async def get(request: Request):
    web_socket_endpoint = ROUTER_PREFIX + WEBSOCKET_PREFIX
    return get_jinja_templates(
        TEMPLATE_NAME,
        {
            "request": request,
            "websocket_endpoint": web_socket_endpoint,
            "user_id": "1",
            "enable_audio_input": "false",
            "enable_audio_output": "true",
            "stop_message": STOP_MESSAGE_PATTERN,
        },
    )

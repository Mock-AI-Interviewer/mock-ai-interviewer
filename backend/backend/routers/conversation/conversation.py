import logging

from fastapi import (APIRouter, Path, Query, Request, WebSocket,
                     WebSocketDisconnect, WebSocketException)
from websockets.exceptions import ConnectionClosedOK

from backend.common import get_jinja_templates
from backend.conf import get_root_package_path
from backend.constants import STOP_MESSAGE_PATTERN
from backend.db.dao import interviews
from backend.routers.conversation.output_handlers import generate_response
from backend.routers.conversation.stream_handlers import (handle_audio_stream,
                                                          handle_text_stream)

LOGGER = logging.getLogger(__name__)
ROUTER_PREFIX = "/interview"
WEBSOCKET_PREFIX = "/response"
TEMPLATE_NAME = "conversation.html"
AUDIO_FILES_DIRECTORY = get_root_package_path()

router = APIRouter(
    prefix="/interview",
    tags=["Interview"],
    responses={},
)


@router.websocket("/{interview_id}/response")
async def conversation_handler(
    websocket: WebSocket,
    interview_id: str = Path(...),
    user_id: str = Query(...),
    enable_audio_input: bool = Query(False),
    enable_audio_output: bool = Query(False),
):
    """
    Handles a WebSocket connection for audio and text data, processing the data accordingly.
    """
    await websocket.accept()

    try:
        while True:
            LOGGER.info("==== Handling generated response ====")
            await generate_response(
                websocket=websocket,
                enable_audio_output=enable_audio_output,
                interview_id=interview_id,
            )

            LOGGER.info("==== Handling user input ====")
            if enable_audio_input:
                await handle_audio_stream(
                    websocket=websocket, user_id=user_id, interview_id=interview_id
                )
            else:
                await handle_text_stream(
                    websocket=websocket, user_id=user_id, interview_id=interview_id
                )

    except ConnectionClosedOK:
        LOGGER.info(f"Connection closed gracefully.")


@router.get("/")
async def get(request: Request):
    web_socket_endpoint = "/Conversation/Response"
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

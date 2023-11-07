import logging
import os

from elevenlabs import generate, play, set_api_key, stream
from fastapi import APIRouter, FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from backend.conf import get_eleven_labs_api_key, get_root_package_path, initialise_app

initialise_app()

LOGGER = logging.getLogger(__name__)
ROUTER_PREFIX = "/interviewer"
WEBSOCKET_PREFIX = "/audio"
DEMO_TEXT = (
    "Hey, I've added some changes that i wasn't planning to merge to main so soon."
)
CHUNK_SIZE = 4000
TEMPLATE_PATH = os.path.join(
    get_root_package_path(), "html_templates", "interviewer.html"
)

router = APIRouter(
    prefix=ROUTER_PREFIX,
    responses={},
)


# WebSocket endpoint
@router.websocket(WEBSOCKET_PREFIX)
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    num_chunks = 0

    # Open a file to save the audio chunks
    with open("./test.mp3", "wb") as f:
        for audio_chunk in generate(
            text=DEMO_TEXT,
            stream_chunk_size=CHUNK_SIZE,
            stream=True,
            latency=1,
        ):
            LOGGER.info(f"Received audio chunk of size: {len(audio_chunk)}")
            num_chunks += 1
            await websocket.send_bytes(audio_chunk)

            # Write the chunk to the file
            f.write(audio_chunk)

    LOGGER.info(f"Number of chunks: {num_chunks}")
    await websocket.close()


@router.get("/")
async def get():
    with open(TEMPLATE_PATH, "r") as f:
        html_content = f.read()
        web_socket_endpoint = ROUTER_PREFIX + WEBSOCKET_PREFIX
        html_content = html_content.replace("/<---WEBSOCKET_ENDPOINT--->/", web_socket_endpoint)
        return HTMLResponse(content=html_content)


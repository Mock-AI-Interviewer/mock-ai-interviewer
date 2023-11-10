import asyncio
import io
import logging
import os

import aiofiles
from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse

from backend.conf import get_root_package_path, initialise_app
from backend.common import get_jinja_templates

initialise_app()

LOGGER = logging.getLogger(__name__)
ROUTER_PREFIX = "/candidate"
WEBSOCKET_PREFIX = "/audio"
AUDIO_FILES_DIRECTORY = get_root_package_path()

router = APIRouter(
    prefix=ROUTER_PREFIX,
    responses={},
)
audio_buffer = io.BytesIO()



@router.websocket(WEBSOCKET_PREFIX)
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    global audio_buffer  # Use the global buffer

    try:
        while True:
            audio_chunk = await websocket.receive_bytes()
            LOGGER.info(f"Received audio chunk of size: {len(audio_chunk)}")
            audio_buffer.write(audio_chunk)  # Append to buffer

            # Transcribe the audio chunk
            # transcripts = await transcribe_audio_chunk(audio_chunk)

            # Send back the transcribed text to the client
            # for text in transcripts:
            #     LOGGER.info(text)
            # await websocket.send_text(text)

            # For example, you can send it back to the client
            await websocket.send_bytes(audio_chunk)
    except WebSocketDisconnect:
        LOGGER.info("WebSocket disconnected normally")
    except Exception as e:
        LOGGER.info(f"Error: {str(e)}")
    finally:
        if audio_buffer:  # If there are any chunks collected, process them
            await process_audio()


# Add a new endpoint to trigger processing
@router.post("/process_audio")
async def process_audio():
    global audio_buffer
    # Ensure we read from the beginning of the buffer
    audio_buffer.seek(0)

    if audio_buffer.getbuffer().nbytes > 0:
        # Generate a file name, for example with a timestamp or a unique ID
        file_name = "audio.wav"  # You can choose the format you prefer
        file_path = file_name

        # text_file_name = "text.txt"
        # text_file_path = text_file_name

        # Save the buffer to a file
        async with aiofiles.open(file_path, "wb") as audio_file:
            await audio_file.write(audio_buffer.getvalue())

        LOGGER.info(f"Saved the audio to {file_path}")

        # open(text_file_path, 'w').close()
        # LOGGER.info(f"Created an empty text file at {text_file_path}")

        # Now, audio_buffer contains all the audio data
        # Send this to Google TTS API
        # transcripts = await transcribe_audio_chunk(audio_buffer)

        # for text in transcripts:
        #     LOGGER.info(text)

        # Reset the buffer for the next audio stream
        audio_buffer = io.BytesIO()

        return {"message": "Audio processing started"}

    else:
        # If buffer is empty, log the information and return a message
        LOGGER.info("Audio buffer is empty. No audio data to save.")
        return {"message": "No audio data to process."}


@router.get("/")
async def get(request: Request):
    web_socket_endpoint = ROUTER_PREFIX + WEBSOCKET_PREFIX
    return get_jinja_templates(
        "candidate.html",
        {"request": request, "websocket_endpoint": web_socket_endpoint}
    )

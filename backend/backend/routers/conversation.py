import logging

from elevenlabs import generate, play, set_api_key, stream
from fastapi import APIRouter, FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from backend.conf import get_eleven_labs_api_key, initialise_app

initialise_app()
LOGGER = logging.getLogger(__name__)

router = APIRouter(
    prefix="/conversation",
    tags=["Web Sockets"],
    responses={},
)


# WebSocket endpoint
@router.websocket("/response")
async def websocket_endpoint(websocket: WebSocket):
    LOGGER.info("--------------WebSocket connection established--------------")
    await websocket.accept()
    num_chunks = 0
    for audio_chunk in generate("Hey, I've added some changes that i wasn't planning to merge to main so soon.", stream=True):
        LOGGER.info(f"Received audio chunk of size: {len(audio_chunk)}")
        num_chunks += 1
        await websocket.send_bytes(audio_chunk)
    LOGGER.info(f"Number of chunks: {num_chunks}")
    await websocket.close()


# HTML response to serve the client page
@router.get("/")
async def get():
    html_content = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <title>Audio Stream</title>
</head>
<body>
    <button id="startButton">Start Audio</button>
    <script>
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const audioQueue = [];
        let isPlaying = false;

        const startButton = document.getElementById('startButton');

        startButton.addEventListener('click', async () => {
            if (audioContext.state === 'suspended') {
                await audioContext.resume();
            }

            const ws = new WebSocket(`ws://${location.host}/conversation/response`);
            ws.binaryType = 'arraybuffer';
            ws.onmessage = async (event) => {
                audioQueue.push(event.data);
                if (!isPlaying) {
                    playAudioQueue();
                }
            };
        });

        let bufferThreshold = 30; // Number of chunks to buffer before playing
        let isBuffering = true; // New flag to manage the buffering state

        async function playAudioQueue() {
            // Start playing if we've reached the buffer threshold or if we're already playing and more data is available
            if ((isBuffering && audioQueue.length >= bufferThreshold) || (!isBuffering && audioQueue.length > 0)) {
                if (isBuffering) {
                    isBuffering = false; // Stop buffering once we start playing
                }
                while (audioQueue.length > 0) {
                    isPlaying = true;
                    const audioData = audioQueue.shift(); // Get the first chunk in the queue
                    await playAudioChunk(audioData);
                }
                isPlaying = false; // Set to false when the queue is empty
            }
        }


        let nextTime = 0; // Tracks when the next audio chunk should start.

        async function playAudioChunk(audioData) {
            try {
                const decodedData = await audioContext.decodeAudioData(audioData.slice(0));
                const source = audioContext.createBufferSource();
                source.buffer = decodedData;
                source.connect(audioContext.destination);

                // Schedule playback to ensure smooth transition between chunks
                const currentTime = audioContext.currentTime;
                const startOffset = nextTime > currentTime ? nextTime : currentTime;
                source.start(startOffset);
                nextTime = startOffset + source.buffer.duration; // Schedule the next chunk

                // Return a promise that resolves when the audio finishes playing
                return new Promise(resolve => source.onended = resolve);
            } catch (e) {
                console.error('Error decoding audio data:', e);
            }
        }

        ws.onmessage = async (event) => {
            audioQueue.push(event.data);
            if (!isPlaying) {
                playAudioQueue(); // Try to play the queue if not already playing
            }
        };
    </script>
</body>
</html>

    """
    return HTMLResponse(content=html_content)

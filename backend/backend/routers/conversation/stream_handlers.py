import logging
import queue
from datetime import datetime
from multiprocessing.pool import ThreadPool

from fastapi import WebSocket
from google.cloud import speech

from backend.conf import get_google_credentials, get_openai_model
from backend.db.dao import interviews_dao
from backend.db.schemas.interviews import (ConversationEntryEmbedded,
                                           ConversationEntryRole)
from backend.routers.conversation.models import (CandidateMessage,
                                                 RecievedStopMessageException,
                                                 is_stop_message)

LOGGER = logging.getLogger(__name__)
SPEECH_CLIENT = speech.SpeechClient(credentials=get_google_credentials())
audio_queue = queue.Queue()
pool = ThreadPool(processes=1)


async def handle_audio_stream(
    websocket: WebSocket, user_id: str, interview_id: str
) -> str:
    """
    Handles incoming audio stream until a stop message is received.
    Returns the full text data based of the transcribed audio.
    """
    try:
        text_chunk = await handle_audio_input(
            websocket=websocket, user_id=user_id, interview_id=interview_id
        )
    except RecievedStopMessageException:
        raise RecievedStopMessageException
    return text_chunk


async def handle_audio_input(
    websocket: WebSocket, user_id: str, interview_id: str
) -> str:
    """
    Handles incoming audio data and converts it to text.
    """
    transcribe_task = None
    start_timestamp = datetime.now()
    while True:
        message = await websocket.receive()
        if "bytes" in message:
            audio_data = message["bytes"]
            LOGGER.info("Sending audio chunk to queue")
            audio_queue.put(audio_data)
            if transcribe_task is None:
                transcribe_task = pool.apply_async(transcribe_audio_data)

        elif "text" in message:
            text_data = message["text"]
            if text_data == "recording_stopped":
                audio_queue.put(None)
                user_response = transcribe_task.get()
                LOGGER.info(f"Final Transcript: {user_response}")
                break

        elif message["type"] == "websocket.disconnect":
            LOGGER.info("WebSocket disconnected")
            break

    # candidate_message = convert_to_candidate_message(text_data)
    LOGGER.info(f"Input: {user_response}")
    end_timestamp = datetime.now()

    interviews_dao.add_message_to_interview_session(
        session_id=interview_id,
        conversation_entry=ConversationEntryEmbedded(
            role=ConversationEntryRole.CANDIDATE.value,
            message=user_response,
            tokens=len(
                user_response.split(" ")
            ),  # TODO Implement token calculation properly
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            model=get_openai_model(),
        ),
    )
    return text_data


def transcribe_audio_data() -> str:
    ret = []
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,  # Adjust the sample rate to match your audio sample rate
        language_code="en-US",  # Change the language code to the language of the audio
        model="video",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    responses = SPEECH_CLIENT.streaming_recognize(
        streaming_config, audio_stream_generator()
    )
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]  # Extract the transcript from the first result
        if result.is_final:
            transcript = result.alternatives[0].transcript
            ret.append(transcript)
            LOGGER.info(f"Transcript: {transcript}")
    LOGGER.info(f"Final Transcript: {' '.join(ret)}")
    return " ".join(ret)


def audio_stream_generator():
    while True:
        LOGGER.info("Stream generator")
        try:
            audio_data = audio_queue.get(timeout=1)
        except queue.Empty:
            continue
        if audio_data is None:
            LOGGER.info("Received sentinel value, ending stream.")
            break

        yield speech.StreamingRecognizeRequest(audio_content=audio_data)
    LOGGER.info("Recording stopped, ending audio stream.")


async def handle_text_stream(
    websocket: WebSocket, user_id: str, interview_id: str
) -> str:
    """
    Handles incoming text stream until a stop message is received.
    Returns the full text data.
    """
    ret = []
    start_timestamp = datetime.now()
    while True:
        try:
            text_chunk = await handle_text_input(websocket, user_id)
            ret.append(text_chunk)
        except RecievedStopMessageException:
            break

    user_response = "".join(ret)
    end_timestamp = datetime.now()

    # Save reponse to db
    interviews_dao.add_message_to_interview_session(
        session_id=interview_id,
        conversation_entry=ConversationEntryEmbedded(
            role=ConversationEntryRole.CANDIDATE.value,
            message=user_response,
            tokens=len(
                user_response.split(" ")
            ),  # TODO Implement token calculation properly
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            model=get_openai_model(),
        ),
    )
    return user_response


async def handle_text_input(websocket: WebSocket, user_id: str) -> str:
    """
    Handles incoming text data.
    If the data is a stop message, raises an exception.
    """
    text_data = await websocket.receive_text()
    candidate_message = convert_to_candidate_message(text_data)
    LOGGER.info(f"Received text data: {candidate_message.data}")
    return candidate_message.data


def convert_to_candidate_message(data: str) -> CandidateMessage:
    """
    Converts the given data to a CandidateMessage.
    Rasies an exception if the data is a stop message.
    """
    candidate_message = CandidateMessage.parse_raw(data)
    if is_stop_message(candidate_message):  # Define how to recognize a stop message
        raise RecievedStopMessageException()
    return candidate_message

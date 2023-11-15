import logging
from datetime import datetime

from fastapi import WebSocket

from backend.conf import get_openai_model
from backend.db.dao import interviews_dao
from backend.db.schemas.interviews import (ConversationEntryEmbedded,
                                           ConversationEntryRole)
from backend.routers.conversation.models import (CandidateMessage,
                                                 RecievedStopMessageException,
                                                 is_stop_message)

LOGGER = logging.getLogger(__name__)
CURRENT_CONVERSATION = interviews_dao.get_last_generated_interview_session().id


async def handle_audio_stream(websocket: WebSocket, user_id: str) -> str:
    """
    Handles incoming audio stream until a stop message is received.
    Returns the full text data based of the transcribed audio.
    """
    ret = []
    while True:
        try:
            text_chunk = await handle_audio_input(websocket, user_id)
            ret.append(text_chunk)
        except RecievedStopMessageException:
            break
    # TODO finish implementation by saving text
    return "".join(ret)


async def handle_audio_input(websocket: WebSocket, user_id: str) -> str:
    """
    Handles incoming audio data and converts it to text.
    """
    audio_data = await websocket.receive_bytes()
    candidate_message = convert_to_candidate_message(audio_data)
    return str(candidate_message.data)[
        :10
    ]  # TODO Dummy implementation, replace with actual implementation that can convert audio to text


async def handle_text_stream(websocket: WebSocket, user_id: str) -> str:
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
        session_id=CURRENT_CONVERSATION,
        conversation_entry=ConversationEntryEmbedded(
            role=ConversationEntryRole.CANDIDATE.value,
            message=user_response,
            tokens=len(user_response.split(" ")),   # TODO Implement token calculation properly
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
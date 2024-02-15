import asyncio
import io
import logging
import os
from datetime import datetime
from typing import Iterator, List
from backend import conf

from fastapi import WebSocket

from backend.db.dao import interviews
from backend.db.models.interviews import (
    ConversationEntryEmbedded,
    ConversationEntryModel,
    ConversationEntryRole,
)
from backend.routers.conversation.models import (
    CandidateMessage,
    InterviewerMessage,
    MessageType,
    is_stop_message,
    send_message,
)
from backend.services import llm as llm_service
from backend.services.eleven_labs.client import speak_sentence

LOGGER = logging.getLogger(__name__)
ASYNCIO_WAIT_TIME = 1

_stop_flag = False


async def generate_response(
    websocket: WebSocket, enable_audio_output: bool, interview_id: str
) -> None:
    start_time = datetime.now()

    # Getting history of messages
    curr_message_hist = llm_service.generate_llm_messages_from_interview_session(
        interview_id
    )

    # Retrieve LLM response. Note this doesn't actually get the resopnse
    # It is a generator that yields the response sentance by sentance
    llm_response = llm_service.get_response_in_sentences(
        messages=curr_message_hist,
        max_tokens=conf.get_llm_max_tokens(),
    )

    # Process LLM response sentence by sentence and return
    send_task = asyncio.create_task(
        send_messages(websocket, llm_response, enable_audio_output)
    )
    listen_task = asyncio.create_task(listen_for_stop(websocket, send_task))
    full_text, _ = await asyncio.gather(send_task, listen_task)

    end_time = datetime.now()
    model = ConversationEntryModel.from_string(llm_service.get_current_model()).value

    # Save reponse to db
    interviews.add_message_to_interview_session(
        interview_id=interview_id,
        conversation_entry=ConversationEntryEmbedded(
            role=ConversationEntryRole.INTERVIEWER.value,
            message=full_text,
            tokens=llm_service.calculate_num_tokens(full_text),
            start_timestamp=start_time,
            end_timestamp=end_time,
            model=model,
        ),
    )


async def send_messages(
    websocket: WebSocket, llm_response: Iterator, enable_audio_output: bool
) -> str:
    """Sends messages to the websocket and returns the full text of the response"""
    global _stop_flag
    full_text = []
    for sentence in llm_response:
        if _stop_flag:
            _stop_flag = False
            break

        sentence_txt = sentence.text
        full_text.append(sentence_txt)

        if not enable_audio_output:
            await send_message(
                websocket, InterviewerMessage(type=MessageType.TEXT, data=sentence_txt)
            )
        else:
            await send_message(
                websocket, InterviewerMessage(type=MessageType.TEXT, data=sentence_txt)
            )
            await speak_sentence(websocket=websocket, sentence=sentence_txt)
        LOGGER.info(f"Sent sentence: {sentence_txt}")

    await send_message(websocket, InterviewerMessage(type=MessageType.STOP, data=""))
    LOGGER.info("Sent Client Stop Message ------------------")
    return "".join(full_text)


async def listen_for_stop(websocket: WebSocket, send_task):
    """Listens for stop message and sets stop_flag if received"""
    global _stop_flag
    while not _stop_flag:
        if send_task.done():
            LOGGER.info("Send messages task completed, exiting listen_for_stop")
            break
        try:
            # using asyncio.wait_for avoids the listen_for_stop coroutine from blocking indefinitely on receive_text()
            text_data = await asyncio.wait_for(
                websocket.receive_text(), timeout=ASYNCIO_WAIT_TIME
            )
            candidate_message = CandidateMessage.parse_raw(text_data)
            if is_stop_message(candidate_message):
                _stop_flag = True
                LOGGER.info("Stop message received.")
                break
        except asyncio.TimeoutError:
            # TimeoutError is expected, so we can ignore it
            pass

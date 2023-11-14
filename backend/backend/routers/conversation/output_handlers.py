import asyncio
import io
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator, List, Union

import aiofiles
from fastapi import (APIRouter, FastAPI, Query, Request, WebSocket,
                     WebSocketDisconnect)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import backend.eleven_labs.client as TTSClient
import backend.openai.client as LLMClient
from backend.conf import (get_jinja_templates_path, get_openai_api_key,
                          get_openai_model, get_openai_organisation,
                          get_root_package_path, initialise_app)
from backend.db.dao import interviews_dao
from backend.db.schemas.interviews import (ConversationEntryEmbedded,
                                           ConversationEntryRole)
from backend.openai.models import GPTMessageEntry, GPTMessages
from backend.constants import STOP_MESSAGE_PATTERN

LOGGER = logging.getLogger(__name__)

ASYNCIO_PAUSE_TIME = 0.1
CURRENT_CONVERSATION = interviews_dao.get_last_generated_interview_session().id


async def generate_response(
    websocket: WebSocket, enable_audio_output: bool
) -> None:
    start_time = datetime.now()

    # Getting history of messages
    curr_message_hist = generate_gpt_messages(session_id=CURRENT_CONVERSATION)

    # Retrieve LLM response. Note this doesn't actually get the resopnse
    # It is a generator that yields the response sentance by sentance
    llm_response = LLMClient.get_response_in_sentences(
        messages=curr_message_hist,
        max_tokens=200,
    )

    # Process LLM response sentance by sentance and return
    full_text = []
    for sentence in llm_response:
        full_text.append(sentence.text)
        sentence_txt = sentence.text
        if not enable_audio_output:
            await websocket.send_text(sentence_txt)
            LOGGER.info(f"Sent text response: {sentence_txt}")
            await asyncio.sleep(ASYNCIO_PAUSE_TIME)  # TODO #37 This is a temporary solution to allow event loop a chance to send data 
        else:
            sentence_txt = TTSClient.clean_sentance(sentence.text)
            await TTSClient.speak_sentance(sentence_txt)
    full_text = "".join(full_text)
    await websocket.send_text(STOP_MESSAGE_PATTERN)

    end_time = datetime.now()

    # Save reponse to db
    interviews_dao.add_message_to_interview_session(
        session_id=CURRENT_CONVERSATION,
        conversation_entry=ConversationEntryEmbedded(
            role=ConversationEntryRole.INTERVIEWER.value,
            message=full_text,
            tokens=LLMClient.get_num_tokens(full_text),
            start_timestamp=start_time,
            end_timestamp=end_time,
            model=get_openai_model(),
        ),
    )



def generate_gpt_messages(session_id: str) -> List[dict]:
    """Generates messages field for use with OpenAI ChatGPT API Calls"""
    interview_session = interviews_dao.get_interview_session_by_id(session_id)
    if not interview_session:
        raise ValueError("Interview session not found.")
    gpt_messages = GPTMessages.from_interview_session(interview_session)
    return gpt_messages.get_messages()
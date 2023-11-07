from dataclasses import dataclass
from typing import Iterator, List

import backend.eleven_labs.client as TTSClient
import backend.openai.client as LLMClient
from backend.conf import (
    get_openai_api_key,
    get_openai_model,
    get_openai_organisation,
    initialise_app,
)
from backend.db.dao import interviews_dao
from backend.openai.models import GPTMessageEntry, GPTMessages
from backend.db.schemas.interviews import (
    ConversationEntryEmbedded,
    ConversationEntryRole,
)
from datetime import datetime

initialise_app()
CURRENT_CONVERSATION = "6547c0499f9250521415d51f"
CURRENT_CONVERSATION = interviews_dao.get_last_generated_interview_session().id



def generate_gpt_messages(session_id: str) -> List[dict]:
    """Generates messages field for use with OpenAI ChatGPT API Calls"""
    interview_session = interviews_dao.get_interview_session_by_id(session_id)
    if not interview_session:
        raise ValueError("Interview session not found.")
    gpt_messages = GPTMessages.from_interview_session(interview_session)
    return gpt_messages.get_messages()


def handle_llm_response():
    start_time = datetime.now()

    curr_message_hist = generate_gpt_messages(session_id=CURRENT_CONVERSATION)

    llm_response = LLMClient.get_response_in_sentences(
        messages=curr_message_hist,
        max_tokens=200,
    )
    full_text = []
    for sentance in llm_response:
        full_text.append(sentance.text)
        sentance_txt = TTSClient.clean_sentance(sentance.text)
        TTSClient.speak_sentance(sentance_txt)
    full_text = "".join(full_text)

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


def handle_user_response():
    # Get USers response to the last sentance
    start_timestamp = datetime.now()
    user_response = input("User Response: ")
    end_timestamp = datetime.now()

    # Save reponse to db
    interviews_dao.add_message_to_interview_session(
        session_id=CURRENT_CONVERSATION,
        conversation_entry=ConversationEntryEmbedded(
            role=ConversationEntryRole.CANDIDATE.value,
            message=user_response,
            tokens=len(user_response.split(" ")),
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            model=get_openai_model(),
        ),
    )


if __name__ == "__main__":
    while(True):
        handle_llm_response()
        handle_user_response()

from dataclasses import dataclass
from typing import List

import backend.ibm_watson.client as TTSClient
import backend.openai.client as LLMClient
from backend.conf import (
    get_openai_api_key,
    get_openai_model,
    get_openai_organisation,
    initialise_app,
)
from backend.db.dao import interviews_dao
from backend.openai.models import GPTMessageEntry, GPTMessages
initialise_app()


def generate_gpt_messages(session_id: str) -> List[dict]:
    """Generates messages field for use with OpenAI ChatGPT API Calls"""
    interview_session = interviews_dao.get_interview_session_by_id(session_id)
    gpt_messages = GPTMessages.from_interview_session(interview_session)
    return gpt_messages.get_messages()


if __name__ == "__main__":
    responses = LLMClient.get_sentance_response(
        messages=generate_gpt_messages(session_id="65479435adfc8de1b792b02e")
    )
    for response in responses:
        cleaned_response = TTSClient.clean_sentance(response.text)
        print(cleaned_response)

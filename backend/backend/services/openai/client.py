import logging
from dataclasses import dataclass
from typing import Generator, List, Optional

from openai import OpenAI

from backend.db.dao import interviews as interviews_dao
from backend.db.models.interviews import InterviewSessionDocument
from backend.models import llm as llm_models
from backend.services.openai import models as openai_models

client = OpenAI()


from backend.conf import get_openai_model

LOGGER = logging.getLogger("openai")
LOGGER.setLevel(logging.INFO)


def get_current_model() -> str:
    """Returns the current OpenAI model"""
    return get_openai_model()


def get_response_in_sentences(
    messages: list,
    model: str,
    sentance_stoppers: list,
    stream: bool,
    max_tokens: int,
    response_format: dict,
) -> Generator[llm_models.SentenceResponse, None, None]:
    """
    Returns a sentance response from the OpenAI API
    Use sentance_stoppers to specify which characters should be used to end a sentance
    """

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=stream,
        max_tokens=max_tokens,
        response_format=response_format,
    )

    full_text = []
    curr_sentance = []
    for chunk in completion:
        finish_reason = chunk.choices[0].finish_reason
        timestamp = chunk.created

        delta = chunk.choices[0].delta
        if delta and delta.content:
            content = delta.content
            curr_sentance.append(content)
            # check if any setance stoppers are in the delta
            if any(stopper in content for stopper in sentance_stoppers):
                curr_str = "".join(curr_sentance)

                yield llm_models.SentenceResponse(
                    text=curr_str, timestamp=timestamp, finish_reason=finish_reason
                )
                # if so, add the current sentance to the full text
                full_text.extend(curr_sentance)
                # and clear the current sentance
                curr_sentance = []


def get_response(
    messages: list, model: str, max_tokens: int, response_format: dict
) -> str:
    """Gets a response from the OpenAI API"""
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        response_format=response_format,
    )
    return completion.choices[0].message.content


def convert_llm_response_format(
    llm_response_format: llm_models.ResponseFormat,
) -> dict:
    """Converts an LLMResponseFormat to the required value for the OpenAI API"""
    if llm_response_format == llm_models.ResponseFormat.TEXT:
        return {"type": "text"}
    elif llm_response_format == llm_models.ResponseFormat.JSON:
        return {"type": "json_object"}
    else:
        raise ValueError(f"Invalid LLMResponseFormat: {llm_response_format}")


def calculate_num_tokens(string: str) -> int:
    """Returns the number of tokens in a string"""
    return len(string.split(" "))


def generate_messages(interview_session: InterviewSessionDocument) -> List[dict]:
    """Generates messages field for use with OpenAI ChatGPT API Calls"""
    gpt_messages = openai_models.GPTMessages.from_interview_session(interview_session)
    return gpt_messages.get_messages()

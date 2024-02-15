"""This module contains the logic for interacting with the LLM API"""
from typing import Generator, List, Optional
from backend import conf

from backend.db.dao import interviews as interviews_dao
from backend.models import llm as llm_models
from backend.services.openai import client as llm_client


def get_current_model() -> str:
    """Returns the current LLM model"""
    return llm_client.get_current_model()


def generate_llm_messages_from_interview_session(interview_id: str) -> List[dict]:
    """Generates messages field for use with LLM API Calls"""
    interview_session = interviews_dao.get_interview_session(interview_id)
    return llm_client.generate_messages(interview_session)


def get_response_in_sentences(
    messages: list,
    model: str = get_current_model(),
    stream: bool = True,
    sentance_stoppers: list = [".", "?", "!", ",", "\n"],
    max_tokens: Optional[int] = None,
    response_format: llm_models.ResponseFormat = llm_models.ResponseFormat.TEXT,
) -> Generator[llm_models.SentenceResponse, None, None]:
    """Gets a response from the LLM API and returns it sentence by sentence"""
    response_format = llm_client.convert_llm_response_format(response_format)
    return llm_client.get_response_in_sentences(
        messages=messages,
        model=model,
        stream=stream,
        sentance_stoppers=sentance_stoppers,
        max_tokens=max_tokens,
        response_format=response_format,
    )


def get_response(
    messages: list,
    model: str = get_current_model(),
    max_tokens=None,
    response_format: llm_models.ResponseFormat = llm_models.ResponseFormat.TEXT,
) -> str:
    """Gets a response from the LLM API"""
    response_format = llm_client.convert_llm_response_format(response_format)
    return llm_client.get_response(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        response_format=response_format,
    )


def calculate_num_tokens(text: str) -> int:
    """Returns the number of tokens in a string"""
    return llm_client.calculate_num_tokens(text)


def convert_sentences_to_string(sentences: List[llm_models.SentenceResponse]) -> str:
    """Converts a list of sentences to a string"""
    return "".join([sentence.text for sentence in sentences])

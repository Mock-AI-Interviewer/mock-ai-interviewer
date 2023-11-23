import logging
from datetime import datetime
from typing import Optional

from backend.converters import interview as model_converter
from backend.db.dao import interviews_dao
from backend.db.schemas.interviews import (
    ConversationEntryModel,
    ConversationEntryRole,
    InterviewSessionDocument,
    is_output_role,
)
from backend.models import interview as models
from backend.services import tokens as tokens_service

LOGGER = logging.getLogger(__name__)


def create_interview_session(
    interview_config: models.InterviewSessionCreate,
) -> models.InterviewSessionRead:
    """Create an interview session with the given configuration"""
    # Check interview type exists
    get_interview_type(interview_config.interview_type.name)

    role = ConversationEntryRole.SYSTEM.value
    init_text = interview_config.interview_type.init_prompt
    tokens = tokens_service.calculate_tokens(init_text)
    current_time = datetime.now()

    interview_session = InterviewSessionDocument(
        interview_type=interview_config.interview_type.dict(),
        user_id=interview_config.user_id,
        conversation_history=[
            {
                "role": role,
                "message": init_text,
                "tokens": tokens,
                "start_timestamp": current_time,
                "end_timestamp": current_time,
            }
        ],
    ).save()

    try:
        interview_id = str(interview_session.id)
        interview_type = model_converter.convert_db_interview_type_to_read(
            interview_session.interview_type
        )
        user_id = str(interview_session.user_id)
        new_interview_session = models.InterviewSessionRead(
            interview_id=interview_id,
            interview_type=interview_type,
            user_id=user_id,
        )
    except Exception as e:
        interview_session.delete()
        raise e

    return new_interview_session


def start_interview(interview_id: str) -> models.InterviewSessionStartedRead:
    """Start an interview session"""
    interview_session = get_interview_session(interview_id)
    start_time = datetime.now()

    interview_session.start_time = start_time
    interview_session.save()

    # Strong type conversion to make sure the read model is correct
    interview_session_read = (
        model_converter.convert_db_interview_session_document_to_read(interview_session)
    )
    return models.InterviewSessionStartedRead(**interview_session_read.dict())


def end_interview(interview_id: str) -> models.InterviewSessionFinishedRead:
    """End an interview session"""
    interview_session = get_interview_session(interview_id)
    end_time = datetime.now()

    interview_session.end_time = end_time
    interview_session.total_input_tokens = calculate_intput_tokens(interview_session)
    interview_session.total_output_tokens = calculate_output_tokens(interview_session)
    interview_session.save()

    # Strong type conversion to make sure the read model is correct
    interview_session_read = (
        model_converter.convert_db_interview_session_document_to_read(interview_session)
    )
    return models.InterviewSessionFinishedRead(**interview_session_read.dict())


def get_interview_type(name: str) -> models.InterviewTypeRead:
    """Get an interview type by name. If no interview type is found, raise exception."""
    interview_type = interviews_dao.get_interview_type(name)
    if not interview_type:
        raise ValueError("Interview type not found.")
    return model_converter.convert_db_interview_type_to_read(interview_type)


def get_interview_session(interview_id: str) -> InterviewSessionDocument:
    """Check if the interview session exists"""
    interview_session = interviews_dao.get_interview_session_by_id(interview_id)
    if not interview_session:
        raise ValueError("Interview session not found.")
    return interview_session


def calculate_intput_tokens(interview_session: InterviewSessionDocument):
    """Calculate the number of tokens the user has inputted"""
    conversation_history = interview_session.conversation_history
    num_tokens = 0
    for conversation_entry in conversation_history:
        if not is_output_role(conversation_entry.role):
            num_tokens += int(conversation_entry.tokens)
    return num_tokens


def calculate_output_tokens(interview_session: InterviewSessionDocument):
    """Calculate the number of tokens the user has outputted"""
    conversation_history = interview_session.conversation_history
    num_tokens = 0
    for conversation_entry in conversation_history:
        if is_output_role(conversation_entry.role):
            num_tokens += int(conversation_entry.tokens)
    return num_tokens

from typing import Optional, Union

from backend.db.models.interviews import (
    InterviewSessionDocument,
    InterviewTypeEmbedded,
    InterviewReviewEmbeedded
)
from datetime import datetime
from backend.models import interviews as models
import logging

LOGGER = logging.getLogger(__name__)

def convert_db_interview_type_to_read(
    interview_type: InterviewTypeEmbedded,
) -> models.InterviewTypeRead:
    """Converts an interview type embedded document to a read model"""
    interview_type_read = models.InterviewTypeRead(
        name=interview_type.name,
        short_description=interview_type.short_description,
        description=interview_type.description,
        job_description=interview_type.job_description,
        init_prompt=interview_type.init_prompt,
        image=interview_type.image,
    )
    return interview_type_read


def convert_db_interview_session_document_to_read(
    interview_session: InterviewSessionDocument,
) -> models.InterviewSessionRead:
    """Converts an  started interview session document to a read model"""
    interview_session_read = models.InterviewSessionRead(
        interview_id=str(interview_session.id),
        interview_type=convert_db_interview_type_to_read(
            interview_session.interview_type
        ),
        user_id=str(interview_session.user_id),
    )

    if interview_session.start_time is not None:
        interview_session_read.start_time = convert_datetime_to_string(
            interview_session.start_time
        )
    if interview_session.end_time is not None:
        interview_session_read.end_time = convert_datetime_to_string(
            interview_session.end_time
        )
    if interview_session.total_output_tokens is not None:
        interview_session_read.total_output_tokens = int(
            interview_session.total_output_tokens
        )
    if interview_session.total_input_tokens is not None:
        interview_session_read.total_input_tokens = int(
            interview_session.total_input_tokens
        )
    if interview_session.review is not None:
        interview_session_read.review = convert_db_interview_review_to_read(
            interview_session.review
        )

    return interview_session_read


def convert_db_interview_review_to_read(
    interview_review: InterviewReviewEmbeedded,
) -> models.InterviewReviewBase:
    """Converts an interview review embedded document to a read model"""
    interview_review_read = models.InterviewReviewBase(
        score=str(interview_review.score), 
        feedback=str(interview_review.feedback)
    )
    return interview_review_read


def convert_datetime_to_string(date: datetime):
    """Converts a datetime object to a string"""
    if date is None:
        return None
    return date.strftime("%Y-%m-%d %H:%M:%S")

from typing import Union

from backend.db.schemas.interviews import (
    InterviewSessionDocument,
    InterviewTypeEmbedded,
)
from backend.models import interview as models


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
) -> Union[
    models.InterviewSessionRead,
    models.InterviewSessionStartedRead,
    models.InterviewSessionFinishedRead,
]:
    """Converts an interview session document to a read model"""
    interview_session_read = models.InterviewSessionRead(
        interview_id=str(interview_session.id),
        interview_type=convert_db_interview_type_to_read(
            interview_session.interview_type
        ),
        user_id=str(interview_session.user_id),
    )

    if interview_session.start_time:
        time = convert_datetime_to_string(interview_session.start_time)
        interview_session_read = models.InterviewSessionStartedRead(
            **interview_session_read.dict(),
            start_time=time,
        )
    if interview_session.end_time:
        time = convert_datetime_to_string(interview_session.end_time)
        interview_session_read = models.InterviewSessionFinishedRead(
            **interview_session_read.dict(),
            end_time=time,
            total_input_tokens=interview_session.total_input_tokens,
            total_output_tokens=interview_session.total_output_tokens,
        )
    return interview_session_read


def convert_datetime_to_string(datetime):
    """Converts a datetime object to a string"""
    return datetime.strftime("%Y-%m-%d %H:%M:%S")

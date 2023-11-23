from typing import List, Optional

from backend.db.schemas.interviews import (
    ConversationEntryEmbedded,
    InterviewSessionDocument,
    InterviewTypeDocument,
)


def get_interview_session_by_id(session_id: str) -> Optional[InterviewSessionDocument]:
    return InterviewSessionDocument.objects.with_id(session_id)


def get_all_interview_types() -> List[InterviewTypeDocument]:
    return list(InterviewTypeDocument.objects.all())


def get_interview_type(name: str) -> Optional[InterviewTypeDocument]:
    """
    Get an interview type by name. Method is case insensitive.
    Returns the first interview type with the given name, or None 
    if no interview type is found.
    """
    return InterviewTypeDocument.objects(name__iexact=name).first()


def add_message_to_interview_session(
    session_id: str, conversation_entry: ConversationEntryEmbedded
) -> None:
    interview_session = InterviewSessionDocument.objects.with_id(session_id)
    if not interview_session:
        raise ValueError("Interview session not found.")
    interview_session.conversation_history.append(conversation_entry)
    interview_session.save()


def get_last_generated_interview_session() -> Optional[InterviewSessionDocument]:
    return InterviewSessionDocument.objects.order_by("-id").first()

from typing import List, Optional
from backend.db.schemas.interviews import (ConversationEntryEmbedded,
                                           InterviewSessionDocument,
                                           InterviewTypeDocument)


def get_interview_session_by_id(session_id: str) -> Optional[InterviewSessionDocument]:
    return InterviewSessionDocument.objects.with_id(session_id)


def get_all_interview_types() -> List[InterviewTypeDocument]:
    return list(InterviewTypeDocument.objects.all())


def add_conversation_entry_to_session(
    session_id: str, conversation_entry: ConversationEntryEmbedded
) -> None:
    interview_session = InterviewSessionDocument.objects.with_id(session_id)
    if not interview_session:
        raise ValueError("Interview session not found.")
    interview_session.conversation_history.append(conversation_entry)
    interview_session.save()

from typing import List, Optional

from backend.db.models.interviews import (ConversationEntryEmbedded,
                                          InterviewReviewEmbeedded,
                                          InterviewSessionDocument,
                                          InterviewTypeDocument,
                                          is_output_role)

from backend.models.interviews import NotFoundError


def get_interview_session(interview_id: str) -> Optional[InterviewSessionDocument]:
    """Get an interview session by id. If the interview session does not exist, raise a 404 error."""
    interview_session = InterviewSessionDocument.objects.with_id(interview_id)
    if not interview_session:
        raise NotFoundError("Interview session not found.")
    return interview_session


def list_all_interview_types() -> List[InterviewTypeDocument]:
    """List all available interview types"""
    return list(InterviewTypeDocument.objects.all())


def get_interview_type(name: str) -> InterviewTypeDocument:
    """
    Get an interview type by name (case insensitive).
    Returns the first interview type with the given name, or raises a 404 error if no interview type is found.
    """
    # Adding __iexact makes search case insensitive
    interview_type = InterviewTypeDocument.objects(name__iexact=name).first()
    if not interview_type:
        raise NotFoundError("Interview type not found.")
    return interview_type


def add_message_to_interview_session(
    interview_id: str, conversation_entry: ConversationEntryEmbedded
) -> InterviewSessionDocument:
    """Add a message to an interview session and update the total number of tokens."""
    interview_session = get_interview_session(interview_id)

    # Updating tokens
    tokens = int(conversation_entry.tokens)
    if is_output_role(conversation_entry.role):
        interview_session.total_output_tokens += tokens
    else:
        interview_session.total_input_tokens += tokens

    interview_session.conversation_history.append(conversation_entry)
    interview_session.save()
    return interview_session

def add_review_to_interview_session(
    interview_id: str, review: InterviewReviewEmbeedded
):
    interview_session = get_interview_session(interview_id)
    interview_session.review = review
    interview_session.save()
    return interview_session


def get_last_generated_interview_session() -> Optional[InterviewSessionDocument]:
    """Get the last generated interview session. If no interview session is found, raise a 404 error."""
    interview_session = InterviewSessionDocument.objects.order_by("-id").first()
    if not interview_session:
        raise NotFoundError("Interview session not found.")
    return interview_session

def delete_last_message_from_interview_session(interview_id: str) -> InterviewSessionDocument:
    interview_session = get_interview_session(interview_id)
    interview_session.conversation_history.pop()
    interview_session.save()
    return interview_session
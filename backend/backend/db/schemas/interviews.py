from enum import Enum, auto

from mongoengine import (DateTimeField, Document, EmbeddedDocument,
                         EmbeddedDocumentField, IntField, ListField,
                         StringField, URLField)


class ConversationEntryRole(Enum):
    INTERVIEWER = "interviewer"
    CANDIDATE = "candidate"
    SYSTEM = "system"


class InterviewTypeBase:
    name = StringField(required=True)
    short_description = StringField(required=True)
    description = StringField(required=True)
    job_description = StringField(required=True)
    init_prompt = StringField(required=True)
    image = URLField(required=True)


class InterviewTypeEmbedded(EmbeddedDocument, InterviewTypeBase):
    pass


class InterviewTypeDocument(Document, InterviewTypeBase):
    meta = {"collection": "interview_types", "indexes": ["name"]}


class ConversationEntryEmbedded(EmbeddedDocument):
    role = StringField(
        required=True, choices=tuple(choice.value for choice in ConversationEntryRole)
    )
    message = StringField(required=True)
    tokens = IntField(required=True)
    start_timestamp = DateTimeField(required=True)
    end_timestamp = DateTimeField(required=True)
    model = StringField(required=True)


class InterviewSessionDocument(Document):
    interview_type = EmbeddedDocumentField(InterviewTypeEmbedded)
    user_id = StringField(required=True)
    start_time = DateTimeField(required=False)
    end_time = DateTimeField(required=False)
    total_input_tokens = IntField(required=False)
    total_output_tokens = IntField(required=False)
    conversation_history = ListField(
        EmbeddedDocumentField(ConversationEntryEmbedded), required=True
    )

    meta = {
        "collection": "interview_sessions",
        "indexes": [
            "user_id",  # Assuming you may want to search or perform lookups by user_id
            "start_time",
            "end_time",
        ],
    }

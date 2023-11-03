from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    ListField,
    EmbeddedDocument,
    EmbeddedDocumentField,
)

class _InterviewTypeBase:
    name = StringField(required=True)
    description = StringField(required=True)
    job_description = StringField(required=True)
    init_prompt = StringField(required=True)

class InterviewTypeEmbedded(EmbeddedDocument, _InterviewTypeBase):
    pass

class InterviewTypeDocument(Document, _InterviewTypeBase):
    meta = {
        'collection': 'interview_types',
        'indexes': ['name']
    }


class ConversationEntryEmbedded(EmbeddedDocument):
    role = StringField(required=True, choices=("interviewer", "candidate"))
    message = StringField(required=True)
    timestamp = DateTimeField(required=True)


class InterviewSessionDocument(Document):
    interview_type = EmbeddedDocumentField(InterviewTypeEmbedded)
    user_id = StringField(required=True)
    start_time = DateTimeField(required=True)
    end_time = DateTimeField(required=True)
    conversation_history = ListField(EmbeddedDocumentField(ConversationEntryEmbedded))

    meta = {
        "collection": "interview_sessions",
        "indexes": [
            "user_id",  # Assuming you may want to search or perform lookups by user_id
            "start_time",
            "end_time",
        ],
    }

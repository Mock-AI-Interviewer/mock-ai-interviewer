from enum import Enum, auto

from mongoengine import (
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    IntField,
    ListField,
    StringField,
    URLField,
)


class ConversationEntryRole(Enum):
    INTERVIEWER = "interviewer"
    CANDIDATE = "candidate"
    SYSTEM = "system"


class InvalidModelError(ValueError):
    """Raised when a unsupported llm model is used"""

    pass


class ConversationEntryModel(Enum):
    GPT_4 = "gpt-4"
    GPT_4_1106_PREVIEW = "gpt-4-1106-preview"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_1106 = "gpt-3.5-turbo-1106"
    NONE = "none"

    @staticmethod
    def from_string(model_str: str):
        for model in ConversationEntryModel:
            if model.value == model_str:
                return model
        raise InvalidModelError(f"Invalid model: {model_str}")


def is_output_role(role: ConversationEntryRole) -> bool:
    return role == ConversationEntryRole.INTERVIEWER.value


class InterviewTypeBase:
    name = StringField(required=True, primary_key=True)
    short_description = StringField(required=True)
    description = StringField(required=True)
    job_description = StringField(required=True)
    init_prompt = StringField(required=True)
    image = URLField(required=True)


class InterviewTypeEmbedded(EmbeddedDocument, InterviewTypeBase):
    pass


class InterviewTypeDocument(Document, InterviewTypeBase):
    meta = {"collection": "interview_types"}


class ConversationEntryEmbedded(EmbeddedDocument):
    role = StringField(
        required=True, choices=tuple(choice.value for choice in ConversationEntryRole)
    )
    message = StringField(required=True)
    tokens = IntField(required=True)
    start_timestamp = DateTimeField(required=True)
    end_timestamp = DateTimeField(required=True)
    model = StringField(
        required=True, choices=tuple(choice.value for choice in ConversationEntryModel)
    )


class InterviewReviewEmbeedded(EmbeddedDocument):
    score = StringField(required=True)
    feedback = StringField(required=True)


class InterviewSessionDocument(Document):
    interview_type = EmbeddedDocumentField(InterviewTypeEmbedded)
    user_id = StringField(required=True)
    start_time = DateTimeField(required=False)
    end_time = DateTimeField(required=False)
    total_input_tokens = IntField(required=False, default=0)
    total_output_tokens = IntField(required=False, default=0)
    conversation_history = ListField(
        EmbeddedDocumentField(ConversationEntryEmbedded), default=[]
    )
    review = EmbeddedDocumentField(InterviewReviewEmbeedded, required=False)

    meta = {
        "collection": "interview_sessions",
        "indexes": [
            "user_id",  # Assuming you may want to search or perform lookups by user_id
            "start_time",
            "end_time",
        ],
    }

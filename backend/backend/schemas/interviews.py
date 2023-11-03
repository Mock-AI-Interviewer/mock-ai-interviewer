from mongoengine import Document, StringField, ReferenceField, DateTimeField, ListField, EmbeddedDocument, EmbeddedDocumentField

class InterviewType(EmbeddedDocument):
    name = StringField(required=True)
    description = StringField(required=True)
    job_description = StringField(required=True)
    init_prompt = StringField(required=True)
    
    meta = {
        'collection': 'interview_types',
        'indexes': [
            'name'  # Assuming you may want to search or perform lookups by name
        ]
    }

# Define an embedded document for the conversation history since it's nested
class ConversationEntry(EmbeddedDocument):
    role = StringField(required=True, choices=('interviewer', 'candidate'))
    message = StringField(required=True)
    timestamp = DateTimeField(required=True)

# Define the InterviewSession with a reference to InterviewType
class InterviewSession(Document):
    interview_type = EmbeddedDocumentField(InterviewType)
    user_id = StringField(required=True)
    start_time = DateTimeField(required=True)
    end_time = DateTimeField(required=True)
    conversation_history = ListField(EmbeddedDocumentField(ConversationEntry))
    
    meta = {
        'collection': 'interview_sessions',
        'indexes': [
            'user_id',  # Assuming you may want to search or perform lookups by user_id
            'start_time',
            'end_time'
        ]
    }

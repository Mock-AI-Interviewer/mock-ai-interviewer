from typing import List

from pydantic import BaseModel, validator

from backend.db.schemas.interviews import ConversationEntryEmbedded, InterviewSessionDocument


class GPTMessageEntry(BaseModel):
    """A message entry for OpenAI ChatGPT API Calls"""

    role: str
    content: str

    # Using a validator to replace the convert_role method
    @validator("role", pre=True, allow_reuse=True)
    def convert_role(cls, role: str) -> str:
        roles = {"interviewer": "assistant", "candidate": "user", "system": "system"}
        if role not in roles:
            raise ValueError(f"Invalid role: {role}")
        return roles[role]


class GPTMessages(BaseModel):
    """A list of message entries for OpenAI ChatGPT API Calls"""

    messages: List[GPTMessageEntry]

    @classmethod
    def from_interview_session(
        cls, interview_session: InterviewSessionDocument
    ) -> "GPTMessages":
        """Creates a GPTMessages object from a list of ConversationEntryEmbedded objects"""
        print(interview_session)
        conversation_history = interview_session.conversation_history
        init_prompt = interview_session.interview_type.init_prompt
        gpt_message_entries = []

        # The initial prompt has a different role
        gpt_message_entries.append(
            GPTMessageEntry(role="system", content=init_prompt)
        )

        # Add the rest of the conversation history
        for conversation_entry in conversation_history:
            message_entry = GPTMessageEntry(
                role=conversation_entry.role, content=conversation_entry.message
            )
            gpt_message_entries.append(message_entry)

        return cls(messages=gpt_message_entries)

    def get_messages(self) -> List[dict]:
        """Returns a list of dictionaries for use with OpenAI ChatGPT API Calls"""
        return [message_entry.dict() for message_entry in self.messages]

from typing import Optional

from pydantic import BaseModel


class InterviewNotStartedError(ValueError):
    """Raised when a user attempts to start an interview that has not started yet"""

    pass

class InterviewNotFinishedError(ValueError):
    """Raised when a user attempts to review an interview that has not finished yet"""

    pass

class InterviewAlreadyReviewedError(ValueError):
    """Raised when a user attempts to review an interview that has already been reviewed"""

    pass

class NotFoundError(ValueError):
    """Raised when a resource is not found in the database"""

    pass

class InterviewTypeBase(BaseModel):
    name: str
    short_description: str
    description: str
    job_description: str
    init_prompt: str
    image: str

class UpdateInitPromptRequest(BaseModel):
    init_prompt: str
class InterviewTypeRead(InterviewTypeBase):
    pass


class InterviewReviewBase(BaseModel):
    """A read model for storing the review of a finished interview session."""

    score: str
    feedback: str


class InterviewSessionBase(BaseModel):
    """A base model for an interview session"""
    interview_type: InterviewTypeBase
    user_id: str
    interview_id: Optional[str] = None
    start_time: Optional[str] = None
    total_input_tokens: Optional[int] = 0
    total_output_tokens: Optional[int] = 0
    end_time: Optional[str] = None
    review: Optional[InterviewReviewBase] = None


class InterviewSessionCreate(InterviewSessionBase):
    """A model for creating an interview session"""

    pass


class InterviewSessionRead(InterviewSessionBase):
    """A read model for an interview session that has not started yet"""

    interview_id: str


class InterviewSessionStartedRead(InterviewSessionRead):
    """A read model for an interview session that has started but not finished"""

    start_time: str
    total_input_tokens: int
    total_output_tokens: int


class InterviewSessionFinishedRead(InterviewSessionStartedRead):
    """A read model for an interview session that has finished"""

    end_time: str


class InterviewSessionReviewRead(InterviewSessionFinishedRead):
    """A read model for an interview session that has been reviewed"""

    review: InterviewReviewBase

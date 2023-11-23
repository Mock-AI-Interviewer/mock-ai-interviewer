from pydantic import BaseModel


class InterviewTypeBase(BaseModel):
    name: str
    short_description: str
    description: str
    job_description: str
    init_prompt: str
    image: str


class InterviewTypeRead(InterviewTypeBase):
    pass


class InterviewSessionBase(BaseModel):
    interview_type: InterviewTypeBase
    user_id: str


class InterviewSessionRead(InterviewSessionBase):
    """A read model for an interview session that has not started yet"""
    interview_id: str


class InterviewSessionStartedRead(InterviewSessionRead):
    """A read model for an interview session that has started but not finished"""
    start_time: str


class InterviewSessionFinishedRead(InterviewSessionStartedRead):
    """A read model for an interview session that has finished"""
    end_time: str
    total_input_tokens: int
    total_output_tokens: int


class InterviewSessionCreate(InterviewSessionBase):
    pass

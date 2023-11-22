from typing import List

from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel

from backend.db.dao import interviews_dao

router = APIRouter(
    prefix="/interview",
    tags=["Interview"],
    responses={},
)


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
    interview_id: str


class InterviewSessionCreate(InterviewSessionBase):
    pass


@router.post("/configure")
async def configure_interview(
    interview_session: InterviewSessionCreate,
) -> InterviewSessionRead:
    """Initialise an interview session with the given configuration"""
    raise NotImplementedError()


@router.get("/types", response_model=List[InterviewTypeRead])
async def list_interview_types():
    all_interview_types = interviews_dao.get_all_interview_types()
    ret = []
    for interview_type in all_interview_types:
        interview_type_read = InterviewTypeRead(
            name=interview_type.name,
            short_description=interview_type.short_description,
            description=interview_type.description,
            job_description=interview_type.job_description,
            init_prompt=interview_type.init_prompt,
            image=interview_type.image,
        )
        ret.append(interview_type_read)
    return ret


@router.get("/types/{name}")
async def get_interview_type(name: str = Path(...)) -> InterviewTypeRead:
    # TODO Change this method to use mongoengine query instead of looping through all interview types
    all_interview_types = interviews_dao.get_all_interview_types()
    for interview_type in all_interview_types:
        if interview_type.name.lower() == name.lower():
            return InterviewTypeRead(
                name=interview_type.name,
                short_description=interview_type.short_description,
                description=interview_type.description,
                job_description=interview_type.job_description,
                init_prompt=interview_type.init_prompt,
                image=interview_type.image,
            )
    raise HTTPException(status_code=404, detail="Interview type not found")


@router.post("/end")
async def end_interview():
    raise NotImplementedError()

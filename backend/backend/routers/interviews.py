import logging
from typing import Optional, List

from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel
from uuid import UUID, uuid4

from backend.converters import interviews as model_converter
from backend.db.dao import interviews as interviews_dao
from backend.models import interviews as models
from backend.services import interviews as service

LOGGER = logging.getLogger(__name__)

router = APIRouter(
    prefix="/interview",
    tags=["Interview"],
    responses={404: {"description": "Not found"}},
)

class Item(BaseModel):
    id: Optional[UUID] = None
    name: str

items = {}

@router.post("/initialise")
async def initialise_interview(
    interview_config: models.InterviewSessionCreate,
) -> models.InterviewSessionRead:
    """Initialise an interview session with the given configuration"""
    try:
        return service.create_interview_session(interview_config)
    except models.NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/session/{interview_id}/start")
async def start_interview(
    interview_id: str = Path(...),
) -> models.InterviewSessionStartedRead:
    """Start an interview session"""
    try:
        return service.start_interview(interview_id)
    except models.NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/session/{interview_id}/review")
async def review_interview(
    interview_id: str = Path(...),
) -> models.InterviewSessionReviewRead:
    """Review an interview session"""
    try:
        return service.review_interview(interview_id)
    except models.NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except models.InterviewNotFinishedError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/session/{interview_id}/end")
async def end_interview(
    interview_id: str = Path(...),
) -> models.InterviewSessionFinishedRead:
    """End an interview session"""
    try:
        return service.end_interview(interview_id)
    except models.NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except models.InterviewNotStartedError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.get("/types", response_model=List[models.InterviewTypeRead])
async def list_interview_types():
    """List all available interview types"""
    return service.list_all_interview_types()


@router.get("/types/{name}")
async def get_interview_type(name: str = Path(...)) -> models.InterviewTypeRead:
    """Get an interview type by name.
    If the interview type does not exist, raise a 404 error."""
    try:
        return service.get_interview_type_read(name)
    except models.NotFoundError as e:
        raise HTTPException(status_code=404, detail="Interview type not found")

@router.get("/session/{interview_id}")
async def get_interview_session(
    interview_id: str = Path(...),
) -> models.InterviewSessionRead:
    """Get an interview session by id.
    If the interview session does not exist, raise a 404 error."""
    try:
        return service.get_interview_type_read(interview_id)
    except models.NotFoundError as e:
        raise HTTPException(status_code=404, detail="Interview session not found")
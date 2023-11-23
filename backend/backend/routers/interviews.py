import logging
from typing import List

from fastapi import APIRouter, HTTPException, Path

from backend.converters import interview as model_converter
from backend.db.dao import interviews_dao
from backend.models import interview as models
from backend.services import interviews as service

LOGGER = logging.getLogger(__name__)

router = APIRouter(
    prefix="/interview",
    tags=["Interview"],
    responses={404: {"description": "Not found"}},
)


@router.post("/initialise")
async def initialise_interview(
    interview_config: models.InterviewSessionCreate,
) -> models.InterviewSessionRead:
    """Initialise an interview session with the given configuration"""
    try:
        return service.create_interview_session(interview_config)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/session/{interview_id}/start")
async def start_interview(
    interview_id: str = Path(...),
) -> models.InterviewSessionStartedRead:
    """Start an interview session"""
    try:
        return service.start_interview(interview_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/session/{interview_id}/end")
async def end_interview(
    interview_id: str = Path(...),
) -> models.InterviewSessionFinishedRead:
    """End an interview session"""
    try:
        return service.end_interview(interview_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/types", response_model=List[models.InterviewTypeRead])
async def list_interview_types():
    """List all available interview types"""
    all_interview_types = interviews_dao.get_all_interview_types()
    ret = []
    for interview_type in all_interview_types:
        interview_type_read = model_converter.convert_db_interview_type_to_read(
            interview_type
        )
        ret.append(interview_type_read)
    return ret


@router.get("/types/{name}")
async def get_interview_type(name: str = Path(...)) -> models.InterviewTypeRead:
    """Get an interview type by name.
    If the interview type does not exist, raise a 404 error."""
    try:
        return service.get_interview_type(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Interview type not found")

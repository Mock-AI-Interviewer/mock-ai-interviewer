import logging
from fastapi import APIRouter, HTTPException, Path, Body

from backend.models import interviews as models
from backend.services import interviews as service

LOGGER = logging.getLogger(__name__)

router = APIRouter(
    prefix="/prompts",
    tags=["Prompt"],
    responses={404: {"description": "Not found"}},
)

@router.put("/{interview_type}")
async def update_interview_type_init_prompt(interview_type: str = Path(...), new_prompt:str = Body(...)) -> models.InterviewTypeRead:
    try:
        return service.update_interview_type_init_prompt(interview_type, new_prompt)
    except models.NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
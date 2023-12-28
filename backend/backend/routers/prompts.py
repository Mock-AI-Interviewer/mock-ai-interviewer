import logging
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel
from uuid import UUID, uuid4

from backend.models import interviews as models
from backend.services import interviews as service

LOGGER = logging.getLogger(__name__)

router = APIRouter(
    prefix="/prompts",
    tags=["Prompt"],
    responses={404: {"description": "Not found"}},
)

@router.put("/{interview_type}/{new_prompt}")
async def update_interview_type_init_prompt(interview_type: str = Path(...),new_prompt: str = Path(...)) -> models.InterviewTypeRead:
    try:
        return service.update_interview_type_init_prompt(interview_type, new_prompt)
    except models.NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
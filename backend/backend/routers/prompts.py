import logging
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel
from uuid import UUID, uuid4

from backend.models import interviews as models
from backend.services import interviews as service

LOGGER = logging.getLogger(__name__)

router = APIRouter(
    prefix="/prompt",
    tags=["Prompt"],
    responses={404: {"description": "Not found"}},
)

class Item(BaseModel):
    id: Optional[UUID] = None
    name: str

items = {}

@router.post("/items/update-prompt/competency/{new_prompt}")
async def update_competency_interview_type_init_prompt(new_prompt: str = Path(...)) -> models.InterviewTypeRead:
    try:
        return service.update_interview_type_init_prompt("Competency", new_prompt)
    except models.NotFoundError as e:
        raise HTTPException(status_code=404, detail="Interview type not found")

@router.post("/items/update-prompt/product-sense/{new_prompt}")
async def update_product_sense_interview_type_init_prompt(new_prompt: str = Path(...)) -> models.InterviewTypeRead:
    try:
        return service.update_interview_type_init_prompt("Product Sense", new_prompt)
    except models.NotFoundError as e:
        raise HTTPException(status_code=404, detail="Interview type not found")

@router.post("/items/update-prompt/coding/{new_prompt}")
async def update_coding_interview_type_init_prompt(new_prompt: str = Path(...)) -> models.InterviewTypeRead:
    try:
        return service.update_interview_type_init_prompt("Coding", new_prompt)
    except models.NotFoundError as e:
        raise HTTPException(status_code=404, detail="Interview type not found")

@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: UUID):
    if item_id in items:
        return items[item_id]
    raise HTTPException(status_code=404, detail="Item not found")

@router.get("/items", response_model=List[models.InterviewTypeSummary])
async def read_all_items():
    return service.list_all_interview_type_summaries()

@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: UUID, item: Item):
    if item_id in items:
        item.id = item_id
        items[item_id] = item
        return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: UUID):
    if item_id in items:
        del items[item_id]
        return {"detail": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")
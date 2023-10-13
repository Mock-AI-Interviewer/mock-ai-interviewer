from datetime import datetime
from datetime import timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi import Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth_backend import current_active_user
from backend.dependencies import get_async_session
from backend.schemas.models import SlotsRead, SlotsCreate
from db.models import Slot, User, UserRole

router = APIRouter(
    prefix="/meetings/slots",
    tags=["Meeting Slots"],
    responses={404: {"description": "Not found"}},
)

SLOT_LENGTH = timedelta(minutes=30)


@router.get("/",
            response_model=List[SlotsRead],
            )
async def list_available_meeting_slots(
        start_time: Optional[datetime] = Query(default=None),
        end_time: Optional[datetime] = Query(default=None),
        session: AsyncSession = Depends(get_async_session)
):
    """Return list of all meeting slots"""
    query = select(Slot)
    if start_time is not None:
        query = query.filter(Slot.start_time >= start_time)
    if end_time is not None:
        query = query.filter(Slot.start_time + timedelta <= end_time)
    # Make sure the slot isn't assigned to a user
    query = query.filter(Slot.user_id == None)
    result = await session.scalars(query)
    slots = result.all()

    return [
        SlotsRead(
            slot_id=slot.uid,
            start_time=slot.start_time,
            end_time=slot.start_time + SLOT_LENGTH,
            advisor_name=slot.advisor_name,
            user_id=slot.user_id,
        )
        for slot in slots
    ]

@router.post("/",
            response_model=SlotsRead,
            )
async def create_meeting_slot(
        current_user: User = Depends(current_active_user),
        slot: SlotsCreate = Body(),
        session: AsyncSession = Depends(get_async_session)
):
    """Create a new meeting slot"""
    if current_user.role == UserRole.NORMAL:
        raise HTTPException(status_code=403, detail="Only advisors or admins can create meeting slots")

    from datetime import timezone

    # Assuming 'slot.start_time' is the offset-aware datetime
    naive_datetime = slot.start_time.astimezone(timezone.utc).replace(tzinfo=None)

    slot = Slot(
        start_time=naive_datetime,
        advisor_name=slot.advisor_name,
    )

    session.add(slot)
    await session.commit()

    return SlotsRead(
        slot_id=slot.uid,
        start_time=slot.start_time,
        end_time=slot.start_time + SLOT_LENGTH,
        advisor_name=slot.advisor_name,
        user_id=slot.user_id,
    )
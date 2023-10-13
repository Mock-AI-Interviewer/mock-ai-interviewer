from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


async def check_user_exists(user_id: int, session: AsyncSession):
    """Checks if a user exists, if not raise an exception"""
    result = await session.scalars(select(User).filter(User.id == user_id))
    user = result.first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

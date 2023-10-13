import json
from datetime import datetime
from random import sample
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Body, Path
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.auth_backend import current_active_user
from backend.dependencies import get_async_session
from backend.routers.meetings import SLOT_LENGTH
from backend.routers.users.calculate_quiz_attempts import SUBJECTS, calculate_quiz_attempts
from backend.schemas.models import QuizAttemptBase, QuestionResponseBase, SlotsRead
from db.models import QuizAttempt, Quiz, QuestionResponse, Slot
from db.models import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/me/quiz_attempts/{quiz_attempt_id}",
            response_model=QuizAttemptBase,
            )
async def get_quiz_attempt(
        current_user: User = Depends(current_active_user),
        quiz_attempt_id: int = Path(...),
        session: AsyncSession = Depends(get_async_session)
):
    """Get a quiz attempt"""

    # Check if quiz attempt exists
    result = await session.scalars(
        select(QuizAttempt)
        .filter(QuizAttempt.uid == quiz_attempt_id)
        .options(joinedload(QuizAttempt.question_responses))
    )
    quiz_attempt = result.first()
    if quiz_attempt is None:
        raise HTTPException(status_code=404, detail="Quiz attempt not found")

    # Check if user owns this quiz attempt
    if quiz_attempt.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="User does not own this quiz attempt")

    return QuizAttemptBase(
        quiz_attempt_id=quiz_attempt.uid,
        user_id=quiz_attempt.user_id,
        quiz_id=quiz_attempt.quiz_id,
        end_time=quiz_attempt.end_time,
        question_responses=__convert_question_responses(quiz_attempt.question_responses),
        subjects=json.loads(quiz_attempt.subjects),
    )


@router.get("/me/quiz_attempts",
            response_model=List[QuizAttemptBase],
            )
async def list_quiz_attempts(
        current_user: User = Depends(current_active_user),
        quiz_id: Optional[int] = Query(default=None),
        session: AsyncSession = Depends(get_async_session)
):
    """List all quiz attempts. Filter by quiz_id if provided"""
    query = (select(QuizAttempt)
             .filter(QuizAttempt.user_id == current_user.id)
             .options(joinedload(QuizAttempt.question_responses))
             )
    if quiz_id is not None:
        query = query.filter(QuizAttempt.quiz_id == quiz_id)

    result = await session.scalars(query)
    quiz_attempts = result.unique().all()

    return [
        QuizAttemptBase(
            quiz_attempt_id=quiz_attempt.uid,
            user_id=quiz_attempt.user_id,
            quiz_id=quiz_attempt.quiz_id,
            end_time=quiz_attempt.end_time,
            question_responses=__convert_question_responses(quiz_attempt.question_responses),
            subjects=json.loads(quiz_attempt.subjects),
        )
        for quiz_attempt
        in quiz_attempts
    ]


@router.post("/me/quiz_attempts", response_model=QuizAttemptBase)
async def calculate_quiz_attempt_results(
        current_user: User = Depends(current_active_user),
        quiz_id: int = Body(...),
        question_responses: List[QuestionResponseBase] = Body(...),
        session: AsyncSession = Depends(get_async_session)
):
    """Calculates the results of a quiz attempt"""
    # Check if quiz exists
    result = await session.scalars(select(Quiz).filter(Quiz.uid == quiz_id))
    quiz = result.first()

    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    subjects = calculate_quiz_attempts(quiz_id, question_responses)

    # Insert Quiz Attempt and Question Responses into DB
    quiz_attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz_id,
        end_time=datetime.now(),
        subjects=json.dumps(subjects),
    )
    session.add(quiz_attempt)
    quiz_attempt.question_responses.extend(
        [
            QuestionResponse(
                question_id=qr.question_id,
                response_id=qr.response_id
            )
            for qr in question_responses
        ]
    )

    await session.commit()

    question_responses_read = __convert_question_responses(quiz_attempt.question_responses)
    # return calculated results
    return QuizAttemptBase(
        quiz_attempt_id=quiz_attempt.uid,
        user_id=quiz_attempt.user_id,
        quiz_id=quiz_attempt.quiz_id,
        end_time=quiz_attempt.end_time,
        question_responses=question_responses_read,
        subjects=json.loads(quiz_attempt.subjects),
    )


@router.get("/me/slots",
            response_model=List[SlotsRead],
            )
async def list_booked_slots(
        current_user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Return list of all a users booked slots"""
    query = select(Slot)
    query = query.filter(Slot.user_id == current_user.id)
    results = await session.scalars(query)
    slots = results.all()

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


# Book a slot for a user
@router.post("/me/slots",
             response_model=SlotsRead,
             )
async def book_slot(
        current_user: User = Depends(current_active_user),
        slot_id: int = Body(...),
        session: AsyncSession = Depends(get_async_session)
):
    """Book a slot for a user"""

    # Check if slot is available
    slot = (await session.scalars(select(Slot).filter(Slot.uid == slot_id))).first()
    if slot is None:
        raise HTTPException(status_code=404, detail="Slot not found")
    if slot.user_id is not None:
        raise HTTPException(status_code=409, detail="Slot already booked")

    # Book slot
    slot.user_id = current_user.id
    await session.commit()

    return SlotsRead(
        slot_id=slot.uid,
        start_time=slot.start_time,
        end_time=slot.start_time + SLOT_LENGTH,
        advisor_name=slot.advisor_name,
        user_id=slot.user_id,
    )


def __convert_question_responses(question_responses: List[QuestionResponse]) -> List[QuestionResponseBase]:
    return [__convert_question_response(qr) for qr in question_responses]


def __convert_question_response(question_response: QuestionResponse) -> QuestionResponseBase:
    return QuestionResponseBase(
        question_id=question_response.question_id,
        response_id=question_response.response_id
    )

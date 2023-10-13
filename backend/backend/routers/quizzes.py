from typing import List

from fastapi import APIRouter, Depends, Body
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.dependencies import get_async_session
from backend.schemas.models import QuizRead, QuestionRead, QuizCreate
from db.models import Quiz, Question

router = APIRouter(
    prefix="/quizzes",
    tags=["Quizzes"],
    responses={404: {"description": "Not found"}},
)


@router.get("/",
            response_model=List[QuizRead],
            )
async def list_quizzes(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    """Returns List of all users"""
    quizzes = (await session.scalars(select(Quiz).offset(skip).limit(limit))).all()
    return [QuizRead(quiz_id=quiz.uid) for quiz in quizzes]


@router.get("/{quiz_id}", response_model=QuizRead)
async def get_quiz(quiz_id: int, session: AsyncSession = Depends(get_async_session)):
    """Returns questions associated with a quiz"""

    # Check if quiz exists
    query = (
        select(Quiz)
        .filter(Quiz.uid == quiz_id)
        .options(
            joinedload(Quiz.questions)
        )
    )
    quiz = (await session.scalars(query)).first()
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    questions = [QuestionRead(question_id=q.uid, question=q.question) for q in quiz.questions]

    quiz_read = QuizRead(
        quiz_id=quiz.uid,
        questions=questions
    )
    return quiz_read


@router.post("/",
             response_model=QuizRead,
             )
async def create_quiz(quiz: QuizCreate = Body(), session: AsyncSession = Depends(get_async_session)):
    """Create a new quiz"""
    questions = [Question(question=q.question) for q in quiz.questions]
    new_quiz = Quiz(
        questions=questions
    )
    session.add(new_quiz)
    await session.commit()
    questions_read = [QuestionRead(question_id=q.uid, question=q.question) for q in new_quiz.questions]

    return QuizRead(quiz_id=new_quiz.uid, questions=questions_read)

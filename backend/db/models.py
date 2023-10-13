from enum import Enum

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship, Session
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class UserRole(str, Enum):
    ADMIN = "admin"
    NORMAL = "normal"
    ADVISOR = "advisor"

class User(SQLAlchemyBaseUserTable[int],Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    role: Mapped[UserRole]

    quiz_attempts: Mapped[List["QuizAttempt"]] = relationship()
    slots: Mapped[List["Slot"]] = relationship()


class Quiz(Base):
    __tablename__ = 'quiz'
    uid: Mapped[int] = mapped_column(primary_key=True)

    questions: Mapped[List["Question"]] = relationship()
    quiz_attempts: Mapped[List["QuizAttempt"]] = relationship()


class Question(Base):
    __tablename__ = 'question'
    uid: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(Integer, ForeignKey('quiz.uid'))
    question: Mapped[str]

    question_responses: Mapped[List["QuestionResponse"]] = relationship()


class Response(Base):
    __tablename__ = 'response'
    uid: Mapped[int] = mapped_column(primary_key=True)
    answer: Mapped[str]

    question_responses: Mapped[List["QuestionResponse"]] = relationship()


class QuizAttempt(Base):
    __tablename__ = 'quiz_attempt'
    uid: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    quiz_id: Mapped[int] = mapped_column(ForeignKey('quiz.uid'))
    end_time: Mapped[datetime]
    subjects: Mapped[str]

    question_responses: Mapped[List["QuestionResponse"]] = relationship()


class Slot(Base):
    __tablename__ = 'slot'
    uid: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('user.id'))
    start_time: Mapped[datetime]
    advisor_name: Mapped[str]


class QuestionResponse(Base):
    __tablename__ = 'question_response'
    quiz_attempt_id: Mapped[int] = mapped_column(ForeignKey('quiz_attempt.uid'), primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('question.uid'), primary_key=True)
    response_id: Mapped[int] = mapped_column(ForeignKey('response.uid'), primary_key=True)



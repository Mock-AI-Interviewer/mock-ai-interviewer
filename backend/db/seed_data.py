from db.models import (Question, User, Quiz,
                       QuizAttempt, Slot, QuestionResponse, Response)
import bcrypt
from db import SessionLocal
from datetime import datetime, timedelta


def seed_data():
    session = SessionLocal()

    # Add a user
    password = b"securepassword"
    # Adding the salt to password
    salt = bcrypt.gensalt()
    # Hashing the password
    hashed = bcrypt.hashpw(password, salt)

    user1 = User(
        email="johndoe@email.com",
        hashed_password=hashed,
        username="JohnDoe",
        name="John Doe Jr",
        password_hash=hashed,
        salt=salt
    )
    session.add(user1)

    # Add a quiz
    quiz1 = Quiz()
    session.add(quiz1)

    # Add questions
    question1 = Question(question="I really like solving logical problems.")
    question2 = Question(question="I need there to be a right answer to a question.")
    question3 = Question(question="I got good grades in the sciences.")
    quiz1.questions.extend([question1, question2, question3])


    # Add a quiz attempt
    quiz_attempt1 = QuizAttempt(
        end_time=datetime.today(),
        subjects='["subject-a", "subject-b", "subject-c"]'
    )
    user1.quiz_attempts.append(quiz_attempt1)
    quiz1.quiz_attempts.append(quiz_attempt1)



    # Adding Responses
    response1 = Response(answer="Strongly Disagree")
    response2 = Response(answer="Disagree")
    response3 = Response(answer="Not Sure")
    response4 = Response(answer="Agree")
    response5 = Response(answer="StronglyAgree")
    session.add_all([response1, response2, response3, response4, response5])

    session.commit()

    # Add question responses
    question_response1 = QuestionResponse(
        quiz_attempt_id=quiz_attempt1.uid,
        question_id=question1.uid,
        response_id=response1.uid
    )
    question_response2 = QuestionResponse(
        quiz_attempt_id=quiz_attempt1.uid,
        question_id=question2.uid,
        response_id=response4.uid
    )
    question_response3 = QuestionResponse(
        quiz_attempt_id=quiz_attempt1.uid,
        question_id=question3.uid,
        response_id=response5.uid
    )
    session.add_all([question_response1, question_response2, question_response3])

    # Add a slot
    slot1 = Slot(
        user_id=user1.id,
        start_time=datetime.today(),
        advisor_name="Dr. Smith"
    )

    slot2 = Slot(
        start_time=datetime.today() - timedelta(days=1),
        advisor_name="Dr. Smith"
    )
    session.add_all([slot1, slot2])

    # Commit the basic objects
    session.commit()

    session.close()


if __name__ == "__main__":
    seed_data()

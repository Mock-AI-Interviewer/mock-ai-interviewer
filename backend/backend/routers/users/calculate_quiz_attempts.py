from enum import Enum
from random import sample
from typing import List

from backend.schemas.models import QuestionResponseBase

SUBJECTS = [
    "Biology",
    "Chemistry",
    "Physics",
    "Mathematics",
    "English Literature",
    "History",
    "Geography",
    "Art and Design",
    "Modern Languages"
]


class Subjects(Enum):
    BIOLOGY = "Biology"
    CHEMISTRY = "Chemistry"
    PHYSICS = "Physics"
    MATHEMATICS = "Mathematics"
    ENGLISH_LITERATURE = "English Literature"
    HISTORY = "History"
    GEOGRAPHY = "Geography"
    ART_AND_DESIGN = "Art and Design"
    MODERN_LANGUAGES = "Modern Languages"


quiz_4_weights = {
    Subjects.BIOLOGY: [0.8, 1, 1, 0, 0, 0, 1, 0, 0.8],
    Subjects.CHEMISTRY: [0.9, 1, 1, 0, 0, 0, 1, 0, 1],
    Subjects.PHYSICS: [1, 1, 0.5, 0, 0, 0, 1, 0, 0.7],
    Subjects.MATHEMATICS: [1, 0.7, 0, 0, 0, 0, 0.9, 0, 0.7],
    Subjects.ENGLISH_LITERATURE: [0, 0, 0, 1, 0.9, 1, 0, 0.5, 0],
    Subjects.HISTORY: [0, 0.7, 0, 0, 1, 0.5, 0, 1, 0],
    Subjects.GEOGRAPHY: [0.5, 1, 0, 0, 1, 0, 0, 0.9, 0],
    Subjects.ART_AND_DESIGN: [0, 0, 0, 1, 0.8, 1, 0, 0.5, 0],
    Subjects.MODERN_LANGUAGES: [0, 0, 0, 0, 1, 0.8, 0, 0, 0]
}

quiz_to_weights_map = {
    4: quiz_4_weights
}


def calculate_quiz_attempts(quiz_id: int, question_responses: List[QuestionResponseBase]) -> List[str]:
    """Takes in list of responses and returns a list of Top 6 subjects"""
    if quiz_id not in quiz_to_weights_map:
        subject_values = [item.value for item in Subjects]
        return sample(subject_values, 6)

    quiz_weights = quiz_to_weights_map[quiz_id]
    subject_totals = {subject: 0 for subject in Subjects}

    # Loop through question responses and calculate subject totals
    for ix, question_response in enumerate(question_responses):
        response = question_response.response_id
        for subject in Subjects:
            subject_totals[subject] += quiz_weights[subject][ix] * response

    sorted_subjects_and_totals = sorted(subject_totals.items(), key=lambda item: item[1], reverse=True)
    print(sorted_subjects_and_totals)
    sorted_subjects_str = [subject.value for subject, total in sorted_subjects_and_totals]

    # Return List of Top 6 subjects
    return sorted_subjects_str[:6]

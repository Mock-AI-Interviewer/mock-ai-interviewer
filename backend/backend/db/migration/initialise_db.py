"""
This script initialises the database with example interview sessions and interview types.
It is intended to be run once, to create the initial database, collections and example documents 
for development.
"""

import json
import logging
import os

from backend.conf import get_root_package_path, initialise_app
from backend.db.models.interviews import InterviewSessionDocument, InterviewTypeDocument

initialise_app()
LOGGER = logging.getLogger(__name__)


def insert_example_interview_session():
    """Inserts an example interview session into the database"""
    json_file_path = os.path.join(
        get_root_package_path(), "db", "examples", "example_interview_sessions.json"
    )
    with open(json_file_path, "r") as file:
        data = json.load(file)
    for item in data:
        session = InterviewSessionDocument(
            **item
        ).save()  # The collection is created here if it doesn"t exist
        LOGGER.info(f"Inserted example interview session with id {session.id}")


def insert_example_interview_types():
    """Inserts example interview types into the database"""
    json_file_path = os.path.join(
        get_root_package_path(), "db", "examples", "example_interview_types.json"
    )
    with open(json_file_path, "r") as file:
        data = json.load(file)
    for item in data:
        session = InterviewTypeDocument(**item)
        session.save()  # The collection is created here if it doesn"t exist
        LOGGER.info(f"Inserted example interview type with id {session.id}")


def insert_example_data():
    insert_example_interview_session()
    insert_example_interview_types()


if __name__ == "__main__":
    insert_example_data()

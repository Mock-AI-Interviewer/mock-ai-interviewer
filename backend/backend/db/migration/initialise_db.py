"""
This script initialises the database with example interview sessions and interview types.
It is intended to be run once, to create the initial database, collections and example documents 
for development.
"""

import json
import os
from mongoengine import connect, DateTimeField, Document
from backend.schemas.interviews import InterviewSessionDocument, InterviewTypeDocument
from backend.conf import ROOT_PATH
import logging

LOGGER = logging.getLogger(__name__)

# Connect to MongoDB (it will create a new database if it doesn"t exist)
db_name = "interview_db"
connect(db_name, host="localhost", port=27017)

def insert_example_interview_session():
    """Inserts an example interview session into the database"""
    json_file_path = os.path.join(ROOT_PATH, "db", "examples", "example_interview_sessions.json")
    with open(json_file_path, "r") as file:
        data = json.load(file)
    for item in data:
        LOGGER.info(item)
        session = InterviewSessionDocument(**item).save()  # The collection is created here if it doesn"t exist
        LOGGER.info(f"Inserted example interview session with id {session.id}")

def insert_example_interview_types():
    """Inserts example interview types into the database"""
    json_file_path = os.path.join(ROOT_PATH, "db", "examples", "example_interview_types.json")
    with open(json_file_path, "r") as file:
        data = json.load(file)
    for item in data:
        session = InterviewTypeDocument(**item)
        session.save()  # The collection is created here if it doesn"t exist
        LOGGER.info(f"Inserted example interview type with id {session.id}")

if __name__ == "__main__":
    insert_example_interview_session()
    insert_example_interview_types()

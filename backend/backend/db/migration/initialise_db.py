import json
import os
from mongoengine import connect
from backend.schemas.interviews import InterviewSession, InterviewType  # import your InterviewSession class
from backend.conf import ROOT_PATH

# Connect to MongoDB (it will create a new database if it doesn"t exist)
db_name = "interview_db"  # Replace with your desired database name
connect(db_name, host="localhost", port=27017)


def insert_example_interview_session():
    json_file_path = os.path.join(ROOT_PATH, "db", "examples", "example_interview_session.json")
    with open(json_file_path, "r") as file:
        data = json.load(file)
    for item in data:
        session = InterviewSession(**item).save()  # The collection is created here if it doesn"t exist

def insert_example_interview_types():
    json_file_path = os.path.join(ROOT_PATH, "db", "examples", "example_interview_types.json")
    with open(json_file_path, "r") as file:
        data = json.load(file)
    for item in data:
        session = InterviewType(**item).save()  # The collection is created here if it doesn"t exist

print(f"Data from JSON has been added to the "{db_name}" database successfully!")

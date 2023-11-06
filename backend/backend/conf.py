import os
from google.oauth2 import service_account
import json


# __file__ is a special variable that holds the path to the current file.
# os.path.realpath() will resolve any symbolic links to the actual file path.
# os.path.dirname() will give you the directory that the file is in.
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

def get_google_service_account_credentials():
    client_file = 'sa-mock-ai-interviewer.json'

    with open(client_file, 'r') as file:
        config = json.load(file)
    config['private_key'] = os.getenv('PRIVATE_KEY').replace('\\n', '\n')
    credentials = service_account.Credentials.from_service_account_file(config)
    return credentials
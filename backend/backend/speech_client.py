from google.cloud import speech
from backend.conf import get_google_service_account_credentials

client = speech.SpeechClient(credentials=get_google_service_account_credentials())
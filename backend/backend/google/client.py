from google.cloud import speech

from backend.conf import get_google_credentials

SPEECH_CLIENT = speech.SpeechClient(credentials=get_google_credentials())

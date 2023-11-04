from google.cloud import speech
from .settings import credentials

client = speech.SpeechClient(credentials=credentials)
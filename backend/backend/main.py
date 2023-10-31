from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# import io
# from google.oauth2 import service_account
# from google.cloud import speech

# client_file = 'sa-mock-ai-interviewer'
# credentials = service_account.Credentials.from_service_account_file(client_file + '.json')
# client = speech.SpeechClient(credentials=credentials)

# Initialise App
app = FastAPI()

# Initialise Users


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can also specify particular origins instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

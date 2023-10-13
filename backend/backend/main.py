from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from backend.auth_backend import auth_backend, fastapi_users, current_active_user
from backend.routers import users, quizzes, meetings
from backend.schemas.models import UserRead, UserCreate, UserUpdate
from db.models import User

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

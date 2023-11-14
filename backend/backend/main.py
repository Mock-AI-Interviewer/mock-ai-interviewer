from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.candidate import router as candidate_speaking_router
from backend.routers.interviewer import router as interviewer_speaking_router
from backend.routers.conversation.conversation import router as conversation_router

app = FastAPI()

app.include_router(candidate_speaking_router)
app.include_router(interviewer_speaking_router)
app.include_router(conversation_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

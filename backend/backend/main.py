from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.websockets import router as websocket_router
from backend.routers.base import router as base_router

app = FastAPI()

app.include_router(websocket_router)
app.include_router(base_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
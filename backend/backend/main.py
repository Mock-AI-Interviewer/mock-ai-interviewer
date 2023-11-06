from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.websocket_routes import websocket_routes
from backend.html_templates import html_templates

app = FastAPI()

app.include_router(websocket_routes)
app.include_router(html_templates)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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

app.include_router(users.router)
app.include_router(quizzes.router)
app.include_router(meetings.router)

# FastAPI User Routers
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

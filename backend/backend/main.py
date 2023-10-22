from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

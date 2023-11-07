# Getting Started with Backend

- THe backend uses [FastAPI](https://fastapi.tiangolo.com/) and [MongoDB](https://www.mongodb.com/) to create a REST API
- Dependency management is done with [Poetry](https://python-poetry.org/)

## Running Locally

- For development on just the backend it's best to run without  kicking up all the docker containers
- You will need to have a MongoDB instance running locally. You can do this by running `docker-compose up -d mongo`
- Next you will need to install Poetry. You can do this by running `pip install poetry`
- Next go to the correct directory (the one with the pyproject.toml) and run `poetry install` to install dependencies
- Run `poetry run uvicorn main:app --reload` to start the server

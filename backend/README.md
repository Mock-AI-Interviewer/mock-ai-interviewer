# Getting Started with Backend

- THe backend uses [FastAPI](https://fastapi.tiangolo.com/) and [MongoDB](https://www.mongodb.com/) to create a REST API
- Dependency management is done with [Poetry](https://python-poetry.org/)

## Running Locally

- For development on just the backend it's best to run without  kicking up all the docker containers
- You will need to have a MongoDB instance running locally. Read the main [README](../README.md) to figure out how to do this
- Next you will need to install Poetry. You can do this by running `pip install poetry`
- Next go to the correct directory (the one with the pyproject.toml) and run `poetry install` to install dependencies
- Next you need to make sure your env variables are set up correctly in the `.env` file
  - You can copy the `.env.example` file and fill in the missing values
  - Read [Setting up DB HOST](#setting-up-db-host) for more information
- *OPTIONAL*: You can clear then populate the db with some example values via the `backend/db/migration/reset.py` script
- Run `poetry run uvicorn main:app --reload` to start the server

### Setting up DB HOST

- For DB_HOST you will need to set it
  - `mongo` - If you're running the backend with `docker-compose.local.yml
  - `mongodb://localhost:27017` - If you're running the backend via `uvicorn`
  - `mongodb+srv://<username>:<password>@<cluster>` - If you're using a cloud instance of MongoDB. Ask the team for the correct values

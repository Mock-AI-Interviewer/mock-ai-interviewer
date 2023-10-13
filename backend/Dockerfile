FROM python:3.9

WORKDIR /backend

# Install Poetry
RUN pip install poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock ./

# Install dependencies without dev dependencies and don't create virtual envs inside Docker
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy the rest of the content
COPY . .

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

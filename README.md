# mock-ai-interviewer

mock-ai-interviewer

## Running locally

- The following section will show you how you can run the project locally

### Prerequisites

- Install Docker and Docker Compose (you can just install Docker Desktop for Windows or Mac)
- If you want to explore the mongo database, install MongoDB Compass

### Steps

- Create .env file in repository root with the following content:

    ```env
    PASSWORD=ANY_PASSWORD
    ```

  - Replace `ANY_PASSWORD` with any password you want
  - In production the actual password will be passed via environment variable

- Run `docker-compose up --build` in repository root
- Open <http://localhost:3000> in your browser

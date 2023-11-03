# Mock AI Interviewer 

- This project is a mock AI interviewer that asks you questions and records your answers 🧠


- The project is split into 3 parts, each with their own respective READMEs:
  - The backend which is responsible for the AI and the database - [README](./backend/README.md)
  - The frontend which is responsible for the UI and the user interaction - [README](./frontend/README.md)
  - The Database which stores the interview types and the conversation history - [README](./backend/backend/db/README.md)

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

- Run `docker-compose up --build` in repository root
- Open <http://localhost:3000> in your browser

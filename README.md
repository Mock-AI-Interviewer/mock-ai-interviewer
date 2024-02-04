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

### Setting up Environment

- Create `.env` file in `./frontend` with the content as shown in the .env.example file:
- Also create a `.env` file in the `./backend` with the content as shown in the .env.example file:
- Fill in missing values with appropriate values

### Running the project Locally

- To run the project a combination of different scripts are used
- Scripts that reference docker compose files are run from the root directory
- Other helper scripts can be found in the `./scripts` directory
- Currently there are 3 progressive ways to run the project

- To run with hot reloading:
  - Doing it this way will allow you to make changes to the code and see the changes reflected in the browser
  - Run `./run-local.sh` and stand up the mongo service
  - Go into the `./backend` directory and run uvicorn with the following command: `uvicorn main:app --reload`
  - Go into the `./frontend` directory and run the following command: `npm start`

- Run project via building containers Locally:
  - Run `./run-local.sh` and stand up all services
  - This utilises the local docker-compose file (`docker-compose.local.yml`)
  
- Run project via the latest hosted containers on ECR (see section below for more details):
  - RUn `./run-test.sh` and stand up all services
  - This utilises the test docker-compose file (`docker-compose.yml`)

### Building Container Images & Pushing to Elastic Container Registry (ECR)

- To do this run the `Build and Push Containers` github action.
- To find out how to trigger this action look at the `on:` section of the `build-and-push-containers.yml` file in the .github/workflows directory
- It should tell you the triggers for the build to be run. ie if it has the `push` trigger, then pushing the branch will trigger the build
- If it has the `workflow_event` trigger, then you can trigger the build manually by going to the actions tab on github and running from there. See [here](https://docs.github.com/en/actions/using-workflows/manually-running-a-workflow?tool=webui#running-a-workflow)

## Running on AWS via Elastic Beanstalk (EB)

### Deploying to Elastic Beanstalk (EB)

- To do this run the `Deploy to Elastic Beanstalk` github action
- To find out how to trigger this action look at the `on:` section of the `build-and-push-containers.yml` file in the .github/workflows directory
- It should tell you the triggers for the build to be run. ie if it has the `push` trigger, then pushing the branch will trigger the build
- If it has the `workflow_event` trigger, then you can trigger the build manually by going to the actions tab on github and running from there. See [here](https://docs.github.com/en/actions/using-workflows/manually-running-a-workflow?tool=webui#running-a-workflow)
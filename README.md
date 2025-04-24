# 🧠 Agent Workshop

## Requirements
- [Docker](https://www.docker.com/)
- [Valid Lambda API Key](https://lambda.ai/inference)

## Setup Instructions  
*(If you are attending the in-person workshop, please checkout to `part_1` or `workshop_part_2` and **ignore the instructions below**.)*

1. Clone the Repository and Checkout the Correct Branch
   ```
   git clone https://github.com/LambdaLabsML/AI_Agent_Masterclass.git
   cd <path_where_cloned_repo_lives>/AI_Agent_Masterclass
   ```

2. Create a `.env` File in the Root Directory
   ```
   LAMBDA_API_BASE="https://api.lambda.ai/v1"
   LAMBDA_API_KEY=<your_lambda_api_key>
   LAMBDA_MODEL="openai/llama-4-maverick-17b-128e-instruct-fp8"
   ```

3. Run with Docker Compose (Recommended)
   ```
   # Default (crews will run async and MLFlow will be launched)
   docker compose up --build

   # Once the container is up and running, you can visit the following link in your browser, to track the execution traces on MLFlow:
   http://0.0.0.0:8000/
   ```

4. (Optional) Run the Crews Synchronously Without MLflow
   ```
   # Build the Docker image
   docker build -f Dockerfile.sync -t ml_agent_workshop_sync .

   # Run the container
   docker run ml_agent_workshop_sync

   # After the Docker Container is finished, get container ID
   docker ps -a

   # Copy reports from container to local machine
   docker cp <container_id>:/app/state_of_the_business/reports <your_local_computer_path>
   ```

4. (Optional) Run the Crews Asynchronously Without MLflow
   ```
   # Build the Docker image
   docker build -f Dockerfile.async -t ml_agent_workshop_async .

   # Run the container
   docker run ml_agent_workshop_async

   # After the Docker Container is finished, get container ID
   docker ps -a

   # Copy reports from container to local machine
   docker cp <container_id>:/app/state_of_the_business/reports <your_local_computer_path>
   ```
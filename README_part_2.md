# 🧠 Agent Workshop

## Requirements
- [Docker](https://www.docker.com/)

## Setup Instructions  

1. Clone the Repository and Checkout the Correct Branch
    ```
    git clone https://github.com/LambdaLabsML/AI_Agent_Masterclass.git
    cd <path_where_cloned_repo_lives>/AI_Agent_Masterclass
    ```

2. Create a `.env` file in the root directory and run the following:
    ```

    cp .env_example .env
    (on windows: copy .env_example .env)
    ```

3. Run the Crews Asynchronously
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

4. Run the Crews Asynchronously with MLFlow
    ```
    # Default (crews will run async and MLFlow will be launched)
    docker compose up --build

    # Once the container is up and running, you can visit the following link in your browser, to track the execution traces on MLFlow:
    http://0.0.0.0:8000/
    ```
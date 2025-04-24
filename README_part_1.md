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

2. Create a `.env` file in the root directory and run the following:
   ```
   cp .env_example .env
   (on windows: copy .env_example .env)
   ```

3. Run the Crews Synchronously
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

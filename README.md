# Agent Workshop

## Setup Instructions

1. Clone the repository
2. Create a `.env` file in the root directory and add the following environment variables:
   ```
   LAMBDA_API_BASE=https://api.lambda.ai/v1
   LAMBDA_API_KEY=<your_lambda_api_key>
   LAMBDA_MODEL="openai/llama-4-maverick"
   ```

3. Run the following Docker commands:

   ```bash
   # Build the Docker image
   docker build -t ml_agent_workshop_image .

   # Run the container
   docker run ml_agent_workshop_image

   # Get container ID
   docker ps -a

   # Copy reports from container to local machine
   docker cp <container_id>:/app/state_of_the_business/reports <your_local_computer_path>
   ```

   Example for copying reports:
   ```bash
   docker cp <container_id>:/app/state_of_the_business/reports /Users/rahul/Desktop/reports
   ```
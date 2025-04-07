# Build stage
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
# Set working directory
WORKDIR /app

# Install UV from official image
COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /bin/uv

# compile Python files to .pyc bytecode files
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy source code and install project
COPY . /app

# Install dependencies and project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Runtime stage
FROM python:3.12-slim-bookworm

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Copy the application from the builder
COPY --from=builder /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Run the application
CMD ["uvicorn", "", "--host", "0.0.0.0", "--port", "$PORT"]

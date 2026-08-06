FROM python:3.11-slim AS builder

# Copy uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Force uv to use system Python so symlinks in .venv resolve in runner
ENV UV_PYTHON_PREFERENCE=only-system \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# 1. Install dependencies
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# 2. Copy source code and sync project
COPY app ./app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM python:3.11-slim AS runner

WORKDIR /app

# Point VIRTUAL_ENV and PATH to virtual environment
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy compiled virtualenv and app code from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/app /app/app

# Create non-root user and grant permissions
RUN groupadd -r appgroup && useradd -r -g appgroup -s /bin/false appuser && \
    chown -R appuser:appgroup /app && \
    chmod -R 755 /app

USER appuser

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
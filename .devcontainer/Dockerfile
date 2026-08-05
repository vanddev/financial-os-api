FROM mcr.microsoft.com/devcontainers/python:1-3.13-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_LINK_MODE=copy

RUN rm -f /etc/apt/sources.list.d/yarn.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && pip install --no-cache-dir uv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

EXPOSE 8000

CMD ["sh", "-c", "uv sync --frozen && exec uv run --no-sync uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"]

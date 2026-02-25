FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY review.py /app/review.py

WORKDIR /app

RUN uv pip install --system --no-cache anthropic>=0.83.0

ENTRYPOINT ["python", "review.py"]

# Built from the repository root (the uv workspace): see infra/docker-compose.yml.
FROM python:3.12-slim

# uv binary, pinned, copied from its official image.
COPY --from=ghcr.io/astral-sh/uv:0.13.8 /uv /bin/uv

WORKDIR /app
# Install only dfoot-api and its dependencies (dfoot-core), exactly as locked,
# without dev tools, as regular (non-editable) packages.
COPY pyproject.toml uv.lock README.md ./
COPY packages ./packages
RUN uv sync --locked --no-dev --no-editable --package dfoot-api

# Don't run as root.
RUN useradd --system dfoot
USER dfoot

EXPOSE 8000
CMD ["/app/.venv/bin/uvicorn", "dfoot_api.main:app", "--host", "0.0.0.0", "--port", "8000"]

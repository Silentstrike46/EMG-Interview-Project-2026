# syntax=docker/dockerfile:1

# Shared uv base. Its Python and Debian release must match the runtime image,
# because the venv built here is copied into it.
FROM ghcr.io/astral-sh/uv:0.12.5-python3.13-trixie-slim AS base

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app


# Runtime venv: dependencies in their own cached layer (rebuilt only when
# pyproject.toml or uv.lock change), then the project itself, non-editable so
# the runtime stage needs no src/ tree.
FROM base AS builder

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev --no-install-project

COPY pyproject.toml uv.lock ./
COPY src ./src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable


# Test image: dev dependencies plus the full source tree, for pytest, ruff and
# mypy. Never used to serve the app.
FROM base AS test

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"

CMD ["pytest"]


# Runtime image (default target, so it is last): the built venv plus what
# Alembic needs to migrate. No uv, no dev dependencies, runs as non-root.
FROM python:3.13-slim-trixie AS runtime

RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY alembic.ini ./
COPY migrations ./migrations

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

USER nonroot

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

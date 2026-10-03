.PHONY: format test run

format:
	uv run ruff check --fix .
	uv run ruff format .

test:
	uv run pytest

run:
	uv run uvicorn backend.main:app --reload

typecheck:
	uv run mypy
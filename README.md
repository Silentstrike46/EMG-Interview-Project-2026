# EMG Formulary

## Requirements

- Docker with Docker Compose v2
- `make` (optional: every `make` command below has a plain `docker compose` equivalent)

## Run

```sh
docker compose up
```

This builds the images, starts Postgres, applies the database migrations, and then starts the API on http://localhost:8000.

- Health check: http://localhost:8000/api/v1/health
- Interactive API docs: http://localhost:8000/docs

Stop with `docker compose down`. The database is kept between runs; add `-v` to delete it.

Shortcuts: `make up` (starts in the background and waits until the API is healthy), `make logs`, `make down`.

## Test

```sh
make test
```

This runs the test suite in a container against its own throwaway Postgres, then removes the test containers. A running `docker compose up` stack is left untouched. It fails if any test fails.

Without `make`:

```sh
docker compose run --build --rm test
```

This leaves the test database container running; remove it with `docker compose rm --stop --force db-test`.

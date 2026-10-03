.PHONY: up down test logs

up:
	docker compose up --build -d --wait

down:
	docker compose --profile test down

# Removes the test containers afterwards, but still fails if pytest fails.
test:
	docker compose run --build --rm test; status=$$?; docker compose --profile test down; exit $$status

logs:
	docker compose logs -f

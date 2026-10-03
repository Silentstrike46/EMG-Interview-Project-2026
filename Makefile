.PHONY: up down test logs

up:
	docker compose up --build -d --wait

down:
	docker compose --profile test down

# Removes only the test database afterwards (the test container goes via --rm),
# leaving a running dev stack alone. Still fails if pytest fails.
test:
	docker compose run --build --rm test; status=$$?; docker compose rm --stop --force db-test; exit $$status

logs:
	docker compose logs -f

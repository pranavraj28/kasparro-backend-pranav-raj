.PHONY: up down test clean logs verify migrate

up:
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 5
	@echo "Services are up! API available at http://localhost:8000"

down:
	docker-compose down

test:
	docker-compose run --rm api pytest tests/ -v

logs:
	docker-compose logs -f api

clean:
	docker-compose down -v
	docker system prune -f

restart:
	docker-compose restart api

shell:
	docker-compose exec api /bin/bash

verify:
	docker-compose run --rm api python verify_setup.py

migrate:
	docker-compose run --rm api alembic upgrade head


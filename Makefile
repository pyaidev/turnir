.PHONY: help dev test lint format type-check clean install migrate migrate-docker

help:
	@echo "Available commands:"
	@echo "  dev          - Start development server with Docker Compose"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linter (ruff)"
	@echo "  format       - Format code (black)"
	@echo "  type-check   - Run type checker (mypy)"
	@echo "  migrate      - Run database migrations locally"
	@echo "  migrate-docker - Run database migrations in Docker"
	@echo "  install      - Install dependencies"
	@echo "  clean        - Clean up containers and volumes"

dev:
	docker compose up --build

test:
	pytest -v

lint:
	ruff check .

format:
	black .

type-check:
	mypy .

migrate:
	alembic upgrade head

migrate-docker:
	docker compose --profile migrate run --rm migrate

install:
	pip install -e .[dev]

clean:
	docker-compose down -v
	docker system prune -f
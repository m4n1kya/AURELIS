.PHONY: help install dev-api dev-frontend batch test lint docker-up docker-down

help:
	@echo "AURELIS Developer Commands"
	@echo "--------------------------"
	@echo "make install       Install Python and Node.js dependencies"
	@echo "make dev-api       Start the FastAPI backend server on port 8000"
	@echo "make dev-frontend  Start the Next.js frontend server on port 3000"
	@echo "make batch         Execute the deterministic CLI engine on dataset/"
	@echo "make test          Run the automated pytest suite"
	@echo "make lint          Run ESLint on the frontend workspace"
	@echo "make docker-up     Build and start full stack via Docker Compose"
	@echo "make docker-down   Stop running Docker Compose containers"

install:
	pip install -r requirements.txt
	cd frontend && npm ci

dev-api:
	python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

dev-frontend:
	cd frontend && npm run dev

batch:
	python engine/run_production.py

test:
	pytest tests/ -v

lint:
	cd frontend && npm run lint

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

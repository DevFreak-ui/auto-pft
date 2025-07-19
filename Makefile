.PHONY: help dev prod build clean logs shell test

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

dev: ## Start development environment
	docker-compose -f docker-compose.dev.yml up --build

dev-d: ## Start development environment in detached mode
	docker-compose -f docker-compose.dev.yml up -d --build

prod: ## Start production environment
	docker-compose up --build -d

build: ## Build all services
	docker-compose build

clean: ## Stop and remove all containers, networks, and volumes
	docker-compose -f docker-compose.dev.yml down -v
	docker-compose down -v
	docker system prune -f

logs: ## View logs from all services
	docker-compose logs -f

logs-dev: ## View logs from development services
	docker-compose -f docker-compose.dev.yml logs -f

shell-backend: ## Access backend container shell
	docker-compose exec backend bash

shell-frontend: ## Access frontend container shell
	docker-compose exec frontend sh

test-backend: ## Run backend tests
	docker-compose exec backend python -m pytest

stop: ## Stop all services
	docker-compose down
	docker-compose -f docker-compose.dev.yml down

restart: ## Restart all services
	docker-compose restart

status: ## Show status of all services
	docker-compose ps


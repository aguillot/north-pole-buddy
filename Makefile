.DEFAULT_GOAL := help

build: ## Run all tests, skipping benchmark tests
	docker compose build --no-cache

shell: ## Run all tests, skipping benchmark tests
	docker compose run --rm npb shell

dev: ## Run all tests, skipping benchmark tests
	docker compose run --service-ports --rm npb_dev dev

test: ## Run all tests, skipping benchmark tests
	docker compose run --rm npb test

lint: ## Run all tests, skipping benchmark tests
	docker compose run --rm npb lint

help: ## Display this help message
	@echo "Makefile help:"
	@echo " make build - Build the project"
	@echo " make shell - Run bash shell inside the container"
	@echo " make test  - Run automated tests"
	@echo " make lint  - Check code style with linting tools"
	@echo " make dev   - Run the local dev server"
	@echo " make help  - Display this help message"
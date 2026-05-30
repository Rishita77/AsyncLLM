PYTHON ?= python
UVICORN ?= uvicorn
APP_MODULE ?= app.main:app

.PHONY: install dev test lint typecheck run docker-up docker-down

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e .[dev]

dev: 
	$(UVICORN) $(APP_MODULE) --reload --host 0.0.0.0 --port 8000

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .

typecheck:
	$(PYTHON) -m mypy app

run:
	$(UVICORN) $(APP_MODULE) --host 0.0.0.0 --port 8000

docker-up:
	docker compose up --build

docker-down:
	docker compose down
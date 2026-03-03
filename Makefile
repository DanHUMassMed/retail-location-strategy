VENV := .venv
PYTHON := $(VENV)/bin/python
RUFF := $(VENV)/bin/ruff
MYPY := $(VENV)/bin/mypy
UV := $(VENV)/bin/uv

.PHONY: dev lint run check-venv

check-venv:
	@test -x $(PYTHON) || (echo "❌ Virtualenv not found. Run: uv sync" && exit 1)

dev:
	uv sync --extra dev

phoenix:
	PHOENIX_HOST=127.0.0.1 PHOENIX_PORT=8081 uv run phoenix serve

lint: check-venv
	$(RUFF) format .
	$(RUFF) check .
	$(MYPY) app/

run: check-venv
	uv run adk web .

run1: check-venv
	@test -n "$(PDF)" || (echo "❌ PDF is required: make run1 PDF=voting_minutes_2025-04-17.pdf" && exit 1)
	$(PYTHON) -m app.cli --file ../data/voting_minutes_pdfs/$(PDF) --output ../data/licenses.json
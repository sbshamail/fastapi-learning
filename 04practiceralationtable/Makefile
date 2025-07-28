SHELL := /bin/bash

run:
	uv run -- uvicorn practice.main:app --reload


generate:
	alembic revision --autogenerate -m "auto"

head:
	alembic upgrade head

reset:
	rm -rf .venv
	uv venv .venv
	source .venv/bin/activate && uv pip install -r pyproject.toml && uv pip install psycopg2-binary




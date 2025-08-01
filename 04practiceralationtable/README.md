# Initialize new project (creates pyproject.toml, main.py, etc.)

## An extremely fast Python package and project manager, written in Rust.

```bash
https://docs.astral.sh/uv/
```

uv init

# Create virtual environment

uv venv

# Activate virtual environment

source .venv/bin/activate

# Add/install dependencies

uv add fastapi uvicorn[standard] sqlmodel

# Install dependencies (sync from lock file)

uv sync

# Run FastAPI app

uv run -- uvicorn practice.main:app --reload

# apt install make for run command ease (for linux)

- create Makefile and define command, follow the syntax must
  make run
  make activate
  make head
  make generate

# install from pyproject.toml

uv pip install -r pyproject.toml

# Update lock file without installing

uv lock

# Clean install (remove unused and reinstall)

uv sync --clean

# alembic

uv add alembic

# if not

source .venv/bin/activate

# for psql install

uv pip install psycopg2-binary

# Alembic

alembic init migrations # start command when not alembic

#

sqlite3 database.db "DROP TABLE alembic_version;"

<!-- install in already project  -->

sqlite3 database.db .dump > backup.sql

- delete db
  alembic revision --autogenerate -m "initial schema"
  alembic upgrade head
- restore data
- remove create table and column in sql replace INSERT INTO user VALUES with INSERT OR IGNORE INTO <model> VALUES
  sqlite3 database.db < backup.sql

## http://localhost:8000/docs

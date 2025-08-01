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

# Update lock file without installing

uv lock

# Clean install (remove unused and reinstall)

uv sync --clean

## http://localhost:8000/docs

FROM python:3.12-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY README.md .
COPY app/ app/
COPY tests/ tests/
COPY alembic/ alembic/
COPY alembic.ini .

# Install dependencies
RUN pip install --no-cache-dir .

# Run migrations and start the application
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
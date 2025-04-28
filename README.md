# Parts API

A REST API for managing parts with CRUD operations and common words analysis.

## Requirements

- Docker and Docker Compose
- Python 3.12+
- Poetry (Python package manager)

## Features

- CRUD operations for parts
- Common words analysis in part descriptions
- Redis caching
- PostgreSQL database
- Docker support

## Setup

1. Create a `.env` file based on `.env.example`
2. Run `docker compose up --build`

## Running Tests

To run the tests locally:

1. Install dependencies with Poetry:
   ```bash
   poetry install
   ```

2. Run the tests:
   ```bash
   poetry run pytest
   ```

   For more detailed test output:
   ```bash
   poetry run pytest -v
   ```

   For test coverage report:
   ```bash
   poetry run pytest --cov=app
   ```

## API Documentation

Once the application is running, you can access the interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

The documentation provides:
- Detailed endpoint descriptions
- Request/response schemas
- Interactive testing interface
- Example requests and responses

## API Endpoints

- `GET /parts/` - List all parts
- `POST /parts/` - Create a new part
- `GET /parts/{part_id}` - Get a specific part
- `PUT /parts/{part_id}` - Update a part
- `DELETE /parts/{part_id}` - Delete a part
- `GET /parts/common-words/` - Get the 5 most common words in part descriptions

# PicPay - User CRUD

A simple and lightweight CRUD API for user management built with FastAPI and SQLAlchemy.

## Project Structure

- `picpay_case/`: Main app (API, models, operations, schemas)
- `tests/`: Unit and integration tests (pytest)
- `Dockerfile`, `docker-compose.yaml`: Docker support
- `pyproject.toml`: Dependencies and scripts (Poetry)

### Project Components

The project is organized for clarity and modularity. Below is an overview of each component and its responsibility:

- [`api/endpoints/`](./picpay_case/api/endpoints/): Contains sub-endpoint route definitions. Each file groups related routes (e.g., users.py handles all user-related endpoints).
- [`api/deps.py`](./picpay_case/api/deps.py): Defines FastAPI dependencies, enabling dependency injection for database sessions, authentication, etc.
- [`core/`](./picpay_case/core/): Holds global configuration. Currently includes config.py, which sets the database URL and related settings.
- [`database.py`](./picpay_case/database.py): Initializes the database connection and SQLAlchemy engine.
- [`main.py`](./picpay_case/main.py): Entry point of the application. It sets up the FastAPI app, defines root paths, includes routers from submodules, and defines the startup event.
- [`models/`](./picpay_case/models/): Defines ORM models. Maps database tables to Python classes using SQLAlchemy (e.g., user.py).
- [`operations/`](./picpay_case/operations/): Encapsulates context-specific business logic. Each module (e.g., user.py) defines a class responsible for handling database interaction and validation logic.
- [`schemas/`](./picpay_case/schemas/): Defines Pydantic models used for request and response validation. Ensures consistent API input/output formats.

### Reference Project Structure

```sh
.
├── picpay_case
│   ├── api
│   │   ├── deps.py
│   │   └── endpoints/
│   │       └── users.py
│   ├── core/
│   │   └── config.py
│   ├── database.py
│   ├── main.py
│   ├── models/
│   │   └── user.py
│   ├── operations/
│   │   └── user.py
│   └── schemas/
│       ├── response.py
│       └── user.py
```

## Running Locally

1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Install dependencies:

   ```sh
   poetry install
   ```

3. Run the API:

   ```sh
   poetry run start
   ```

The API will be available at http://localhost:8000.

Built-in interactive documentation (Swagger UI) is accessible at http://localhost:8000/docs.

## Running with Docker

The project includes a multi-stage Dockerfile for lightweight images and a docker-compose.yaml for orchestrating containers.

```sh
docker-compose up --build
```

## Running Tests

Tests are split into function-specific and API-specific, organized similarly to the main project structure.

Run tests with:

```sh
poetry run pytest tests -v
```

## API

### Healh Endpoints

- `/health` basic status / liveness check
- `/ping` just returns `pong`
- `/` welcome message and reference to api documentation

### User Endpoints

- `GET /users/` - List all users
- `GET /users/{id}` - Get user by ID
- `POST /users/` - Create a new user
- `PUT /users/{id}` - Update existing user
- `DELETE /users/{id}` - Remove user by ID

# Employee Management System

A modular, production-ready RESTful API for managing employee records, built with Flask, SQLAlchemy, and Pydantic. This project demonstrates best practices in Python backend development, including layered architecture, validation, error handling, and automated testing.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Code Flow](#code-flow)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Setup & Installation](#setup--installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Environment Variables](#environment-variables)
- [License](#license)

---

## Project Structure

```
.
├── app/                # Main application package
│   ├── __init__.py     # App factory, extension and blueprint registration
│   ├── exceptions.py   # Custom exception classes
│   ├── extensions.py   # Flask extensions (db, API spec)
│   ├── run.py          # Entrypoint for running the app
│   ├── controllers/    # API route handlers (Blueprints)
│   ├── middleware/     # Request/response logging middleware
│   ├── models/         # SQLAlchemy ORM models
│   ├── repositories/   # Data access layer (CRUD, queries)
│   ├── schemas/        # Pydantic schemas for validation/serialization
│   ├── services/       # Business logic layer
│   └── utils/          # Error handler registration
├── tests/              # Unit and integration tests
├── config.py           # App configuration (reads from .env)
├── requirements.txt    # Python dependencies
├── pytest.ini          # Pytest configuration
├── pyproject.toml      # Linting/formatting config (Ruff)
├── conftest.py         # Pytest fixtures for app and client
├── .env                # Environment variables (example provided)
```

---

## Code Flow

1. **App Initialization**:  
   - `app/__init__.py` creates the Flask app, loads config, initializes extensions, registers blueprints, middleware, and error handlers.

2. **Request Handling**:  
   - Requests hit endpoints defined in `app/controllers/employee_controller.py`.
   - Input is validated using Pydantic schemas (`app/schemas/employee_schema.py`).
   - Business logic is handled in `app/services/employee_service.py`.
   - Data is accessed via the repository layer (`app/repositories/employee_repository.py`), which interacts with the SQLAlchemy model (`app/models/employee.py`).

3. **Middleware & Error Handling**:  
   - Logging middleware logs each request/response (`app/middleware/logging_middleware.py`).
   - Custom error handlers in `app/utils/error_handlers.py` return consistent JSON errors for validation, business, and server errors.

4. **Testing**:  
   - Tests in `tests/` use Pytest, with fixtures in `conftest.py` for isolated, in-memory database testing.

---

## API Endpoints

All endpoints are prefixed with `/employees`.

| Method | Endpoint                | Description                        |
|--------|-------------------------|------------------------------------|
| POST   | `/employees/`           | Create a new employee              |
| GET    | `/employees/`           | List employees (with filters)      |
| GET    | `/employees/<id>`       | Get employee by ID                 |
| PUT    | `/employees/<id>`       | Update employee by ID              |
| DELETE | `/employees/<id>`       | Delete employee by ID              |

### Query Parameters for Listing

- `page` (int): Page number (default: 1)
- `page_size` (int): Records per page (default: 10)
- `department` (str): Filter by department
- `sort` (str): Field to sort by (e.g., `name`, `salary`)
- `order` (str): `asc` or `desc`
- `min_salary` (float): Minimum salary
- `max_salary` (float): Maximum salary

### Example Request

```http
GET /employees/?department=IT&sort=salary&order=desc&page=1&page_size=5
```

---

## Database Schema

**Table: `employees`**

| Column      | Type         | Constraints           |
|-------------|--------------|-----------------------|
| id          | Integer      | Primary Key, AutoInc  |
| name        | String(120)  | Not Null              |
| email       | String(120)  | Unique, Not Null      |
| department  | String(100)  | Nullable              |
| date_joined | DateTime     | Not Null, Default Now |
| salary      | Float        | Nullable              |

---

## Setup & Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/sanskarvijpuria/Employee-Management-System.git
   cd Employee_Management_System
   ```

2. **Create and configure your environment:**
   - Copy `.env.example` to `.env` and update values as needed (especially database credentials).

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   - For development, you can use SQLite or configure MySQL as per `.env`.
   - To initialize tables:
     ```sh
     flask --app app/run.py init-db
     ```

---

## Running the Application

```sh
# Set environment variables if not using .env
export FLASK_ENV=development
export FLASK_APP=app/run.py

# Run the Flask app
flask run
```
Or, to run directly:
```sh
python app/run.py
```
The API will be available at `http://localhost:5000`.

---

## Running with Docker

This project is fully containerized using Docker and Docker Compose, allowing for a consistent development and production environment.

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running the Application

1.  **Build and Run the Containers:**
    From the project root, run the following command:
    ```sh
    docker-compose up --build
    ```
    This command will:
    - Build the Docker image for the Flask application based on the `Dockerfile`.
    - Start the `web` (Flask app) and `db` (MySQL) services.
    - Automatically run the `flask init-db` command to create the database tables.
    - Start the Gunicorn web server.

2.  **Access the Application:**
    The API will be available at `http://localhost:5000`.

### Stopping the Application

To stop and remove the containers, networks, and volumes, run: `docker-compose down -v`

## Running Tests

1. **Ensure all dependencies are installed.**
2. **Run tests with coverage:**
   ```sh
   pytest
   ```
   or for a coverage report:
   ```sh
   pytest --cov=app --cov-report=term-missing --cov-report=html
   ```
   - Coverage HTML report will be in `htmlcov/`.

---

## Environment Variables

- `FLASK_ENV`: Flask environment (`development`, `production`)
- `FLASK_APP`: Entry point (e.g., `app/run.py`)
- `SECRET_KEY`: Secret key for Flask
- `PORT`: Port to run the app (default: 5000)
- `DATABASE_URL`: Full SQLAlchemy DB URI (overrides individual DB_* vars)
- `DB_USERNAME`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`: Used to construct DB URI if `DATABASE_URL` is not set

---

## License

This project is for educational and demonstration purposes.

---

**Feel free to open issues or contribute!**

# Task Management API

A RESTful API for managing Employees and Tasks, built with FastAPI and PostgreSQL, following a professional and scalable project structure.

## Features

- **Employees**: Full CRUD with Search (Name, Role).
- **Tasks**: Full CRUD with Search (Title, Description) and Filtering.
- **Users**: Full CRUD.
- **Company Overview**: Fetch all employees and tasks in a single request.
- **Dashboard Stats**: Real-time statistics for tasks and employees.
- **Authentication**: JWT-based authentication for sensitive operations.
- **Modular Design**: Organized for scalability and maintainability.

## Tech Stack

- **Language**: Python 3.9+
- **Framework**: FastAPI
- **Database**: PostgreSQL (Async via asyncpg)
- **ORM**: SQLAlchemy
- **Authentication**: OAuth2 with JWT (python-jose)

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:
    - The `.env` file is already pre-configured with the Neon DB credentials.
    - If needed, copy `.env.example` to `.env` and update values manually.

5.  **Run the application**:
    ```bash
    uvicorn app.main:app --reload
    ```

## Testing & Seeding

A Jupyter Notebook `api_tests.ipynb` is provided to seed data and test the API.

1.  **Start the server** (as shown above).
2.  **Open the notebook**:
    ```bash
    jupyter notebook api_tests.ipynb
    ```
    (Or use VS Code's Jupyter extension)
3.  **Run all cells** to seed users, employees, and tasks, and verify the endpoints.

## API Documentation

Once the application is running, you can access the interactive API documentation at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Endpoints

### Auth
- `POST /api/v1/login/access-token`: Login to get an access token.

### Company
- `GET /api/v1/company/overview`: Get all employees and tasks.

### Stats
- `GET /api/v1/stats/dashboard`: Get dashboard statistics (Total tasks, Tasks by status, Total employees).

### Users
- `POST /api/v1/users/`: Register a new user.
- `GET /api/v1/users/`: List all users (Protected).
- `GET /api/v1/users/{id}`: Get a specific user (Protected).
- `PUT /api/v1/users/{id}`: Update a user (Protected).
- `DELETE /api/v1/users/{id}`: Delete a user (Protected).

### Employees
- `GET /api/v1/employees/`: List all employees (supports `search`).
- `POST /api/v1/employees/`: Create a new employee.
- `GET /api/v1/employees/{id}`: Get a specific employee.
- `PUT /api/v1/employees/{id}`: Update an employee.
- `DELETE /api/v1/employees/{id}`: Delete an employee.

### Tasks
- `GET /api/v1/tasks/`: List tasks (supports `search`, `status`, `employee_id`).
- `POST /api/v1/tasks/`: Create a new task (Authenticated).
- `GET /api/v1/tasks/{id}`: Get a specific task.
- `PUT /api/v1/tasks/{id}`: Update a task (Authenticated).
- `DELETE /api/v1/tasks/{id}`: Delete a task (Authenticated).

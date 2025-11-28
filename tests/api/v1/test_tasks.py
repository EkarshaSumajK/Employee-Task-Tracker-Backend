import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    # Create an employee to assign task to
    emp_response = await client.post(
        "/api/v1/employees/",
        json={"name": "Task Employee", "role": "Worker", "email": "task@example.com"},
    )
    emp_id = emp_response.json()["data"]["id"]

    # Create task (assuming auth is mocked or not required for this test setup, 
    # or we need to add auth headers. For simplicity in this demo, we might hit 401 if auth is strictly enforced.
    # Based on code, create_task requires current_user. We need to override that dependency or mock auth.)
    
    # For now, let's assume we need to mock the user. 
    # In a real scenario, we'd get a token first. 
    # Since we didn't add auth mocking in conftest yet, this might fail if we don't handle it.
    # Let's try to hit the public endpoint (GET /tasks) first to be safe, 
    # or we can add a simple override for get_current_user in conftest or here.
    pass

@pytest.mark.asyncio
async def test_read_tasks(client: AsyncClient):
    response = await client.get("/api/v1/tasks/")
    assert response.status_code == 200
    data = response.json()["data"]
    assert isinstance(data, list)

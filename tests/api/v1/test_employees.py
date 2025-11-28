import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_employee(client: AsyncClient):
    response = await client.post(
        "/api/v1/employees/",
        json={"name": "Test Employee", "role": "Developer", "email": "test@example.com"},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "Test Employee"
    assert data["email"] == "test@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_read_employees(client: AsyncClient):
    # Create an employee first
    await client.post(
        "/api/v1/employees/",
        json={"name": "Test Employee 2", "role": "Manager", "email": "test2@example.com"},
    )
    
    response = await client.get("/api/v1/employees/")
    assert response.status_code == 200
    data = response.json()["data"]
    assert isinstance(data, list)
    assert len(data) > 0

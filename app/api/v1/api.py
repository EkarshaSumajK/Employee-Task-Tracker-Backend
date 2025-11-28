from fastapi import APIRouter
from app.api.v1.endpoints import login, users, employees, tasks, stats, company

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
api_router.include_router(company.router, prefix="/company", tags=["company"])

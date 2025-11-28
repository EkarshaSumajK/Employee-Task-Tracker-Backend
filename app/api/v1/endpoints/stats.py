from typing import Any, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy.future import select
from app.api import deps
from app.models.task import Task, TaskStatus
from app.models.employee import Employee
from app import schemas

router = APIRouter()

@router.get("/dashboard", response_model=schemas.Response[Dict[str, Any]])
async def get_dashboard_stats(
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Get dashboard statistics:
    - Total tasks
    - Tasks by status
    - Total employees
    """
    # Total Tasks
    total_tasks_query = select(func.count(Task.id))
    total_tasks = (await db.execute(total_tasks_query)).scalar()

    # Tasks by Status
    tasks_by_status = {}
    for status in TaskStatus:
        query = select(func.count(Task.id)).filter(Task.status == status.value)
        count = (await db.execute(query)).scalar()
        tasks_by_status[status.value] = count

    # Total Employees
    total_employees_query = select(func.count(Employee.id))
    total_employees = (await db.execute(total_employees_query)).scalar()

    return {
        "status": 200,
        "data": {
            "total_tasks": total_tasks,
            "tasks_by_status": tasks_by_status,
            "total_employees": total_employees
        }
    }

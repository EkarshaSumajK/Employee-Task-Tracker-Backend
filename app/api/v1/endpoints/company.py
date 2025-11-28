from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/overview", response_model=schemas.Response[schemas.CompanyOverview])
async def get_company_overview(
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Get all employees and tasks for the company.
    """
    employees = await crud.get_employees(db)
    tasks = await crud.get_tasks(db)
    
    return {
        "status": 200,
        "data": {
            "employees": employees,
            "tasks": tasks
        }
    }

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas, models
from app.api import deps

router = APIRouter()

@router.get("/", response_model=schemas.Response[List[schemas.Employee]])
async def read_employees(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
) -> Any:
    employees = await crud.get_employees(db, skip=skip, limit=limit, search=search)
    return {"status": 200, "data": employees}

@router.post("/", response_model=schemas.Response[schemas.Employee])
async def create_employee(
    *,
    db: AsyncSession = Depends(deps.get_db),
    employee_in: schemas.EmployeeCreate,
) -> Any:
    employee = await crud.get_employee_by_email(db, email=employee_in.email)
    if employee:
        raise HTTPException(
            status_code=400,
            detail="The employee with this email already exists in the system.",
        )
    employee = await crud.create_employee(db, employee=employee_in)
    return {"status": 200, "data": employee}

@router.get("/{employee_id}", response_model=schemas.Response[schemas.Employee])
async def read_employee(
    *,
    db: AsyncSession = Depends(deps.get_db),
    employee_id: int,
) -> Any:
    employee = await crud.get_employee(db, employee_id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"status": 200, "data": employee}

@router.put("/{employee_id}", response_model=schemas.Response[schemas.Employee])
async def update_employee(
    *,
    db: AsyncSession = Depends(deps.get_db),
    employee_id: int,
    employee_in: schemas.EmployeeUpdate,
    # current_user: models.User = Depends(deps.get_current_user), # Optional: Protect this
) -> Any:
    employee = await crud.get_employee(db, employee_id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee = await crud.update_employee(db, db_employee=employee, employee=employee_in)
    return {"status": 200, "data": employee}

@router.delete("/{employee_id}", response_model=schemas.Response[schemas.Employee])
async def delete_employee(
    *,
    db: AsyncSession = Depends(deps.get_db),
    employee_id: int,
    # current_user: models.User = Depends(deps.get_current_user), # Optional: Protect this
) -> Any:
    employee = await crud.get_employee(db, employee_id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee = await crud.delete_employee(db, db_employee=employee)
    return {"status": 200, "data": employee}

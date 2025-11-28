from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Task])
async def read_tasks(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[schemas.TaskStatus] = None,
    employee_id: Optional[int] = None,
    search: Optional[str] = None,
) -> Any:
    status_str = status.value if status else None
    tasks = await crud.get_tasks(db, skip=skip, limit=limit, status=status_str, employee_id=employee_id, search=search)
    return tasks

@router.post("/", response_model=schemas.Task)
async def create_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    task_in: schemas.TaskCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    task = await crud.create_task(db, task=task_in)
    return task

@router.put("/{task_id}", response_model=schemas.Task)
async def update_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    task_id: int,
    task_in: schemas.TaskUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    task = await crud.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task = await crud.update_task(db, db_task=task, task=task_in)
    return task

@router.get("/{task_id}", response_model=schemas.Task)
async def read_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    task_id: int,
) -> Any:
    task = await crud.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", response_model=schemas.Task)
async def delete_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    task_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    task = await crud.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task = await crud.delete_task(db, db_task=task)
    return task

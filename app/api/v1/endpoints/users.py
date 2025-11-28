from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas, models
from app.api import deps

router = APIRouter()

@router.get("/", response_model=schemas.Response[List[schemas.User]])
async def read_users(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    users = await crud.get_users(db, skip=skip, limit=limit)
    return {"status": 200, "data": users}

@router.post("/", response_model=schemas.Response[schemas.User])
async def create_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    user = await crud.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await crud.create_user(db, user=user_in)
    return {"status": 200, "data": user}

@router.get("/{user_id}", response_model=schemas.Response[schemas.User])
async def read_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    user = await crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": 200, "data": user}

@router.put("/{user_id}", response_model=schemas.Response[schemas.User])
async def update_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    user = await crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = await crud.update_user(db, db_user=user, user=user_in)
    return {"status": 200, "data": user}

@router.delete("/{user_id}", response_model=schemas.Response[schemas.User])
async def delete_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    user = await crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = await crud.delete_user(db, db_user=user)
    return {"status": 200, "data": user}

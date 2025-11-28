from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

async def get(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).filter(Task.id == task_id))
    return result.scalars().first()

async def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100, status: str = None, employee_id: int = None, search: str = None):
    query = select(Task)
    if status:
        query = query.filter(Task.status == status)
    if employee_id:
        query = query.filter(Task.employee_id == employee_id)
    if search:
        search_filter = f"%{search}%"
        query = query.filter((Task.title.ilike(search_filter)) | (Task.description.ilike(search_filter)))
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def create(db: AsyncSession, task: TaskCreate):
    db_task = Task(**task.dict())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def update(db: AsyncSession, db_task: Task, task: TaskUpdate):
    update_data = task.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def remove(db: AsyncSession, db_task: Task):
    await db.delete(db_task)
    await db.commit()
    return db_task

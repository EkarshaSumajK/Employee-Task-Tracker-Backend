from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

async def get(db: AsyncSession, employee_id: int):
    result = await db.execute(select(Employee).options(selectinload(Employee.tasks)).filter(Employee.id == employee_id))
    return result.scalars().first()

async def get_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(Employee).options(selectinload(Employee.tasks)).filter(Employee.email == email))
    return result.scalars().first()

async def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100, search: str = None):
    query = select(Employee).options(selectinload(Employee.tasks))
    if search:
        search_filter = f"%{search}%"
        query = query.filter((Employee.name.ilike(search_filter)) | (Employee.role.ilike(search_filter)))
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def create(db: AsyncSession, employee: EmployeeCreate):
    db_employee = Employee(name=employee.name, role=employee.role, email=employee.email)
    db.add(db_employee)
    await db.commit()
    await db.refresh(db_employee)
    # Re-fetch to load tasks
    return await get(db, db_employee.id)

async def update(db: AsyncSession, db_employee: Employee, employee: EmployeeUpdate):
    update_data = employee.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_employee, key, value)
    
    db.add(db_employee)
    await db.commit()
    await db.refresh(db_employee)
    # Re-fetch to load tasks
    return await get(db, db_employee.id)

async def remove(db: AsyncSession, db_employee: Employee):
    await db.delete(db_employee)
    await db.commit()
    return db_employee

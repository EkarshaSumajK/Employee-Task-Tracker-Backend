import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User
from app.models.employee import Employee
from sqlalchemy.future import select
from app.models.task import Task, TaskStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def seed_data():
    async with SessionLocal() as db:
        try:
            # 1. Seed Users
            logger.info("Seeding Users...")
            test_user = await db.execute(select(User).filter(User.username == "admin"))
            if not test_user.scalars().first():
                user = User(username="admin", hashed_password=get_password_hash("admin123"))
                db.add(user)
            
            # 2. Seed Employees
            logger.info("Seeding Employees...")
            employees_data = [
                {"name": "Alice Johnson", "role": "Backend Developer", "email": "alice@example.com"},
                {"name": "Bob Smith", "role": "Frontend Developer", "email": "bob@example.com"},
                {"name": "Charlie Brown", "role": "Project Manager", "email": "charlie@example.com"},
            ]
            
            created_employees = []
            for emp_data in employees_data:
                # Check if exists
                existing = await db.execute(select(Employee).filter(Employee.email == emp_data["email"]))
                existing_emp = existing.scalars().first()
                if not existing_emp:
                    new_emp = Employee(**emp_data)
                    db.add(new_emp)
                    created_employees.append(new_emp)
                else:
                    created_employees.append(existing_emp)
            
            await db.commit() # Commit to get IDs
            
            # Refresh to ensure we have IDs
            for emp in created_employees:
                await db.refresh(emp)

            # 3. Seed Tasks
            logger.info("Seeding Tasks...")
            if created_employees:
                tasks_data = [
                    {"title": "Fix API Authentication", "description": "JWT token not validating correctly", "status": TaskStatus.PENDING.value, "employee_id": created_employees[0].id},
                    {"title": "Design Dashboard UI", "description": "Create wireframes for the main dashboard", "status": TaskStatus.IN_PROGRESS.value, "employee_id": created_employees[1].id},
                    {"title": "Sprint Planning", "description": "Prepare for next sprint", "status": TaskStatus.COMPLETED.value, "employee_id": created_employees[2].id},
                    {"title": "Database Optimization", "description": "Index optimization for queries", "status": TaskStatus.PENDING.value, "employee_id": created_employees[0].id},
                ]

                for task_data in tasks_data:
                    # Simple check to avoid duplicates (optional, based on title)
                    existing_task = await db.execute(select(Task).filter(Task.title == task_data["title"]))
                    if not existing_task.scalars().first():
                        db.add(Task(**task_data))
            
            await db.commit()
            logger.info("Seeding Completed Successfully!")

        except Exception as e:
            logger.error(f"Error seeding data: {e}")
            await db.rollback()

if __name__ == "__main__":
    asyncio.run(seed_data())

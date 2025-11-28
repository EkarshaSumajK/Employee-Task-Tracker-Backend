from typing import List, Optional
from pydantic import BaseModel, EmailStr
from .task import Task

class EmployeeBase(BaseModel):
    name: str
    role: str
    email: EmailStr

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    email: Optional[EmailStr] = None

class Employee(EmployeeBase):
    id: int
    tasks: List[Task] = []

    class Config:
        from_attributes = True

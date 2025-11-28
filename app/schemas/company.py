from typing import List
from pydantic import BaseModel
from .employee import Employee
from .task import Task

class CompanyOverview(BaseModel):
    employees: List[Employee]
    tasks: List[Task]

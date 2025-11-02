from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    department: Optional[str] = None
    salary: Optional[float] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    department: Optional[str]
    salary: Optional[float]

class EmployeeResponse(EmployeeBase):
    id: int
    join_date: Optional[datetime]

    class Config:
        from_attributes = True

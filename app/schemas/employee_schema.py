"""
This module defines Pydantic schemas for employee data validation and serialization.
Schemas are used for request/response validation in API endpoints.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# ---------------------------------------------------------------------------
# Base Schema (common fields)
# ---------------------------------------------------------------------------
class EmployeeBase(BaseModel):
    """
    Base schema for employee fields.

    Attributes:
        name (str): Full name of the employee.
        email (EmailStr): Employee email address (must be unique).
        department (str | None): Department name.
        salary (float | None): Monthly salary of the employee.
    """

    name: str = Field(..., min_length=1, max_length=120, description="Full name of the employee")
    email: EmailStr = Field(..., description="Employee email address (must be unique)")
    department: str | None = Field(None, description="Department name")
    salary: float | None = Field(None, ge=0, description="Monthly salary of the employee")


# ---------------------------------------------------------------------------
# Create / Update Schemas
# ---------------------------------------------------------------------------
class EmployeeCreate(EmployeeBase):
    """
    Schema for creating a new employee.
    Inherits all fields from EmployeeBase.
    """

    pass


class EmployeeUpdate(BaseModel):
    """
    Schema for updating employee details.

    All fields are optional and validated if provided.
    """

    name: str | None = Field(None, min_length=1, max_length=120)
    email: EmailStr | None = None
    department: str | None = None
    salary: float | None = Field(None, ge=0)


class EmployeeResponse(EmployeeBase):
    """
    Schema returned for an employee record in API responses.

    Attributes:
        id (int): Unique employee ID.
        date_joined (datetime): Date of joining.
    """

    id: int = Field(..., description="Unique employee ID")
    date_joined: datetime = Field(..., description="Date of joining")

    class Config:
        from_attributes = True  # allows returning ORM objects directly


class EmployeesListResponse(BaseModel):
    """
    Paginated list of employees for list endpoints.

    Attributes:
        total (int): Total number of employees.
        employees (list[EmployeeResponse]): List of employee records.
    """

    total: int
    employees: list[EmployeeResponse]


class DeleteEmployeeResponse(BaseModel):
    """
    Schema for confirmation message after employee deletion.

    Attributes:
        message (str): Confirmation message.
    """

    message: str = Field(..., description="Confirmation message after deletion")


class EmployeeQueryParams(BaseModel):
    """
    Query parameters for employee list endpoint.

    Attributes:
        page (int): Page number for pagination.
        page_size (int): Number of records per page.
        department (str | None): Filter by department.
        sort (str | None): Field to sort by.
        order (str | None): Sorting order (asc or desc).
        min_salary (float | None): Minimum salary filter.
        max_salary (float | None): Maximum salary filter.
    """

    page: int = Field(1, ge=1, description="Page number for pagination")
    page_size: int = Field(10, ge=1, le=100, description="Number of records per page")
    department: str | None = Field(None, description="Filter by department")
    sort: str | None = Field(None, description="Field to sort by (e.g. name, salary)")
    order: str | None = Field(None, description="Sorting order (asc or desc)")
    min_salary: float | None = Field(None, ge=0, description="Minimum salary filter")
    max_salary: float | None = Field(None, ge=0, description="Maximum salary filter")

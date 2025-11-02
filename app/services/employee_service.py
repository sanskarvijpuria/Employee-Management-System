"""
This module provides the EmployeeService class, which implements business logic for employee operations.
It acts as a service layer between the API routes and the data repository.
"""

from typing import Any

from app.exceptions import DuplicateEmailError, EmployeeNotFound
from app.models.employee import Employee
from app.repositories.employee_repository import employee_repository


class EmployeeService:
    """
    Business logic layer for employee operations.
    Provides methods for creating, retrieving, updating, and deleting employees.
    """

    def __init__(self, repository):
        """
        Initialize the EmployeeService.

        Args:
            repository: The repository instance for data access.
        """
        self.repository = repository

    def create_employee(self, data: dict[str, Any]) -> Employee:
        """
        Create a new employee record.

        Args:
            data (dict): Dictionary of employee fields.

        Returns:
            Employee: The created employee instance.

        Raises:
            DuplicateEmailError: If an employee with the same email already exists.
        """
        if self.repository.get_by_email(data["email"]):
            raise DuplicateEmailError(f"Employee with email '{data['email']}' already exists.")

        employee = Employee(**data)
        return self.repository.create(employee)

    def list_employees(self, filters: dict[str, Any] | None = None) -> tuple[list[Employee], int]:
        """
        Retrieve all employees with optional filters, pagination, and sorting.

        Args:
            filters (dict, optional): Filtering, sorting, and pagination options.

        Returns:
            tuple[list[Employee], int]: List of employees and total count.
        """
        return self.repository.get_all(filters)

    def get_employee(self, emp_id: int) -> Employee:
        """
        Retrieve an employee by ID.

        Args:
            emp_id (int): Employee ID.

        Returns:
            Employee: The employee instance.

        Raises:
            EmployeeNotFound: If no employee with the given ID exists.
        """
        employee = self.repository.get_by_id(emp_id)
        if not employee:
            raise EmployeeNotFound(f"Employee with ID {emp_id} not found.")
        return employee

    def update_employee(self, emp_id: int, data: dict[str, Any]) -> Employee:
        """
        Update an existing employee record.

        Args:
            emp_id (int): Employee ID.
            data (dict): Fields to update.

        Returns:
            Employee: The updated employee instance.

        Raises:
            DuplicateEmailError: If updating to an email that already exists.
        """
        employee = self.get_employee(emp_id)

        # Check for email uniqueness if email is being updated
        if "email" in data and data["email"] != employee.email:
            if self.repository.get_by_email(data["email"]):
                raise DuplicateEmailError(f"Employee with email '{data['email']}' already exists.")

        for key, value in data.items():
            setattr(employee, key, value)

        return self.repository.update(employee)

    def delete_employee(self, emp_id: int) -> None:
        """
        Delete an employee by ID.

        Args:
            emp_id (int): Employee ID.

        Returns:
            None
        """
        employee = self.get_employee(emp_id)
        self.repository.delete(employee)


# Instantiate the service for dependency injection
employee_service = EmployeeService(repository=employee_repository)

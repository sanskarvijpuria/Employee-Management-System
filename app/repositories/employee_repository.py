"""
This module provides the EmployeeRepository class for database operations on Employee records.
It encapsulates CRUD operations and query logic for the Employee model.
"""

from sqlalchemy import asc, desc

from app.extensions import db
from app.models.employee import Employee


class EmployeeRepository:
    """
    Repository class for Employee model database operations.
    Provides methods for CRUD and query operations on employees.
    """

    def get_all(self, filters: dict | None = None) -> tuple[list[Employee], int]:
        """
        Retrieve employees with optional filters, pagination, and sorting.

        Args:
            filters (dict, optional): Filtering, sorting, and pagination options.

        Returns:
            tuple[list[Employee], int]: List of employees and total count.
        """
        query = Employee.query

        # Apply filters
        if filters:
            if filters.get("department"):
                query = query.filter(Employee.department == filters["department"])

            if filters.get("min_salary") is not None:
                query = query.filter(Employee.salary >= float(filters["min_salary"]))

            if filters.get("max_salary") is not None:
                query = query.filter(Employee.salary <= float(filters["max_salary"]))

            # Sorting
            sort_field = filters.get("sort")
            order = filters.get("order", "asc")
            if sort_field and hasattr(Employee, sort_field):
                query = query.order_by(
                    desc(getattr(Employee, sort_field))
                    if order.lower() == "desc"
                    else asc(getattr(Employee, sort_field))
                )

        # Pagination
        filters = filters or {}
        page = int(filters.get("page", 1))
        page_size = int(filters.get("page_size", 10))

        total = query.count()
        employees = query.offset((page - 1) * page_size).limit(page_size).all()
        return employees, total or 0

    def get_by_id(self, emp_id: int) -> Employee | None:
        """
        Retrieve an employee by ID.

        Args:
            emp_id (int): Employee ID.

        Returns:
            Employee | None: Employee instance or None if not found.
        """
        return Employee.query.get(emp_id)

    def get_by_email(self, email: str) -> Employee | None:
        """
        Retrieve an employee by email address.

        Args:
            email (str): Employee email.

        Returns:
            Employee | None: Employee instance or None if not found.
        """
        return Employee.query.filter_by(email=email).first()

    def create(self, employee: Employee) -> Employee:
        """
        Add a new employee to the database.

        Args:
            employee (Employee): Employee instance to add.

        Returns:
            Employee: The created employee instance.
        """
        db.session.add(employee)
        db.session.commit()
        return employee

    def update(self, employee: Employee) -> Employee:
        """
        Commit changes to an existing employee.

        Args:
            employee (Employee): Employee instance with updated fields.

        Returns:
            Employee: The updated employee instance.
        """
        db.session.commit()
        return employee

    def delete(self, employee: Employee) -> None:
        """
        Delete an employee from the database.

        Args:
            employee (Employee): Employee instance to delete.

        Returns:
            None
        """
        db.session.delete(employee)
        db.session.commit()


# Instantiate the repository for dependency injection
employee_repository = EmployeeRepository()

"""
This module defines the Flask Blueprint and route handlers for employee-related API endpoints.
It provides endpoints for creating, retrieving, updating, and deleting employees.
All endpoints are documented and validated using FlaskPydanticSpec.
"""

from flask import Blueprint, request
from flask_pydantic_spec import Request, Response

from app.extensions import spec
from app.schemas.employee_schema import (
    DeleteEmployeeResponse,
    EmployeeCreate,
    EmployeeQueryParams,
    EmployeeResponse,
    EmployeesListResponse,
    EmployeeUpdate,
)
from app.services.employee_service import employee_service

employee_bp = Blueprint("employee", __name__)


@employee_bp.route("/", methods=["POST"])
@spec.validate(
    body=Request(EmployeeCreate),
    resp=Response(HTTP_201=EmployeeResponse),
    tags=["Employees"],
)
def create_employee():
    """
    Create a new employee.

    Request Body:
        EmployeeCreate: Pydantic model with employee details.

    Returns:
        Tuple (dict, int): JSON response with created employee data and HTTP 201 status.
    """
    data = request.context.body.dict()  # type: ignore[attr-defined]
    employee = employee_service.create_employee(data)
    return EmployeeResponse.from_orm(employee).model_dump(mode="json"), 201


@employee_bp.route("/", methods=["GET"])
@spec.validate(
    query=EmployeeQueryParams,
    resp=Response(HTTP_200=EmployeesListResponse),
    tags=["Employees"],
)
def get_all_employees():
    """
    List all employees with optional pagination and filtering.

    Query Parameters:
        EmployeeQueryParams: Pydantic model for filtering and pagination.

    Returns:
        Tuple (dict, int): JSON response with list of employees and HTTP 200 status.
    """
    filters = request.context.query.dict()  # type: ignore[attr-defined]
    employees, total = employee_service.list_employees(filters)
    response = EmployeesListResponse(
        total=total,
        employees=[EmployeeResponse.from_orm(e) for e in employees],
    )
    return response.model_dump(mode="json"), 200


@employee_bp.route("/<int:emp_id>", methods=["GET"])
@spec.validate(resp=Response(HTTP_200=EmployeeResponse), tags=["Employees"])
def get_employee(emp_id):
    """
    Retrieve a specific employee by ID.

    Args:
        emp_id (int): Employee ID.

    Returns:
        Tuple (dict, int): JSON response with employee data and HTTP 200 status.
    """
    employee = employee_service.get_employee(emp_id)
    return EmployeeResponse.from_orm(employee).model_dump(mode="json"), 200


@employee_bp.route("/<int:emp_id>", methods=["PUT"])
@spec.validate(
    body=Request(EmployeeUpdate),
    resp=Response(HTTP_200=EmployeeResponse),  # This should return the updated employee
    tags=["Employees"],
)
def update_employee(emp_id):
    """
    Update an existing employee by ID.

    Args:
        emp_id (int): Employee ID.
    Request Body:
        EmployeeUpdate: Pydantic model with fields to update.

    Returns:
        Tuple (dict, int): JSON response with updated employee data and HTTP 200 status.
    """
    data = request.context.body.dict(exclude_unset=True)  # type: ignore[attr-defined]
    updated_employee = employee_service.update_employee(emp_id, data)
    return EmployeeResponse.from_orm(updated_employee).model_dump(mode="json"), 200


@employee_bp.route("/<int:emp_id>", methods=["DELETE"])
@spec.validate(resp=Response(HTTP_200=DeleteEmployeeResponse), tags=["Employees"])
def delete_employee(emp_id):
    """
    Delete an employee by ID.

    Args:
        emp_id (int): Employee ID.

    Returns:
        Tuple (dict, int): JSON response with deletion message and HTTP 200 status.
    """
    employee_service.delete_employee(emp_id)
    return (
        DeleteEmployeeResponse(
            message=f"Employee with ID {emp_id} deleted successfully."
        ).model_dump(mode="json"),
        200,
    )

from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.services.employee_service import EmployeeService
from app.schemas.employee_schema import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
)

employee_bp = Blueprint("employee", __name__, url_prefix="/employees")


@employee_bp.route("/", methods=["GET"])
def get_all_employees():
    employees = EmployeeService.list_employees()
    result = [EmployeeResponse.model_validate(e).model_dump() for e in employees]
    return jsonify(result), 200


@employee_bp.route("/<int:emp_id>", methods=["GET"])
def get_employee(emp_id):
    employee = EmployeeService.get_employee(emp_id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404
    data = EmployeeResponse.model_validate(employee).model_dump()
    return jsonify(data), 200


@employee_bp.route("/", methods=["POST"])
def create_employee():
    try:
        data = EmployeeCreate.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    employee = EmployeeService.create_employee(data.model_dump())
    response = EmployeeResponse.model_validate(employee)
    return jsonify(response.model_dump()), 201


@employee_bp.route("/<int:emp_id>", methods=["PUT"])
def update_employee(emp_id):
    try:
        data = EmployeeUpdate.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    updated = EmployeeService.update_employee(emp_id, data.model_dump(exclude_unset=True))
    if not updated:
        return jsonify({"error": "Employee not found"}), 404

    response = EmployeeResponse.model_validate(updated)
    return jsonify(response.model_dump()), 200


@employee_bp.route("/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    success = EmployeeService.delete_employee(emp_id)
    if not success:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify({"message": "Employee deleted"}), 200

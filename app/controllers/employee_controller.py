from flask import Blueprint, jsonify, request
from app.services.employee_service import EmployeeService

employee_bp = Blueprint("employee", __name__, url_prefix="/employees")


@employee_bp.route("/", methods=["GET"])
def get_all_employees():
    employees = EmployeeService.list_employees()
    result = [
        {
            "id": e.id,
            "first_name": e.first_name,
            "last_name": e.last_name,
            "email": e.email,
            "department": e.department,
            "salary": e.salary,
            "join_date": e.join_date.isoformat() if e.join_date else None,
        }
        for e in employees
    ]
    return jsonify(result), 200


@employee_bp.route("/<int:emp_id>", methods=["GET"])
def get_employee(emp_id):
    employee = EmployeeService.get_employee(emp_id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify({
        "id": employee.id,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "email": employee.email,
        "department": employee.department,
        "salary": employee.salary,
        "join_date": employee.join_date.isoformat() if employee.join_date else None,
    }), 200


@employee_bp.route("/", methods=["POST"])
def create_employee():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    employee = EmployeeService.create_employee(data)
    return jsonify({"id": employee.id, "message": "Employee created"}), 201


@employee_bp.route("/<int:emp_id>", methods=["PUT"])
def update_employee(emp_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    updated = EmployeeService.update_employee(emp_id, data)
    if not updated:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify({"message": "Employee updated"}), 200


@employee_bp.route("/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    success = EmployeeService.delete_employee(emp_id)
    if not success:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify({"message": "Employee deleted"}), 200

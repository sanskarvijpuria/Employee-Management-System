from app.models.employee import Employee
from app.extensions import db

class EmployeeRepository:
    @staticmethod
    def get_all():
        return Employee.query.all()

    @staticmethod
    def get_by_id(emp_id: int):
        return Employee.query.get(emp_id)

    @staticmethod
    def create(employee_data: dict):
        employee = Employee(**employee_data)
        db.session.add(employee)
        db.session.commit()
        return employee

    @staticmethod
    def update(emp_id: int, updates: dict):
        employee = Employee.query.get(emp_id)
        if not employee:
            return None
        for key, value in updates.items():
            setattr(employee, key, value)
        db.session.commit()
        return employee

    @staticmethod
    def delete(emp_id: int):
        employee = Employee.query.get(emp_id)
        if not employee:
            return False
        db.session.delete(employee)
        db.session.commit()
        return True

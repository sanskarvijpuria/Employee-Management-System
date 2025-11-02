from app.repositories.employee_repository import EmployeeRepository

class EmployeeService:
    @staticmethod
    def list_employees():
        return EmployeeRepository.get_all()

    @staticmethod
    def get_employee(emp_id):
        return EmployeeRepository.get_by_id(emp_id)

    @staticmethod
    def create_employee(data):
        return EmployeeRepository.create(data)

    @staticmethod
    def update_employee(emp_id, data):
        return EmployeeRepository.update(emp_id, data)

    @staticmethod
    def delete_employee(emp_id):
        return EmployeeRepository.delete(emp_id)

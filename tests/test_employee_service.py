from unittest.mock import MagicMock

import pytest

from app.exceptions import DuplicateEmailError, EmployeeNotFound
from app.models.employee import Employee
from app.services.employee_service import EmployeeService


@pytest.fixture
def mock_repository():
    """Fixture for a mocked employee repository."""
    return MagicMock()


@pytest.fixture
def employee_service(mock_repository):
    """Fixture for the EmployeeService with a mocked repository."""
    return EmployeeService(repository=mock_repository)


def test_create_employee_success(employee_service, mock_repository):
    """Test successful creation of an employee."""
    employee_data = {"name": "John Doe", "email": "john.doe@example.com"}
    mock_repository.get_by_email.return_value = None
    mock_repository.create.return_value = Employee(id=1, **employee_data)

    new_employee = employee_service.create_employee(employee_data)

    mock_repository.get_by_email.assert_called_once_with("john.doe@example.com")
    assert new_employee is not None
    assert new_employee.name == "John Doe"


def test_create_employee_duplicate_email(employee_service, mock_repository):
    """Test creating an employee with a duplicate email raises an error."""
    employee_data = {"name": "John Doe", "email": "john.doe@example.com"}
    mock_repository.get_by_email.return_value = Employee(id=1, **employee_data)

    with pytest.raises(DuplicateEmailError):
        employee_service.create_employee(employee_data)

    mock_repository.create.assert_not_called()


def test_get_employee_success(employee_service, mock_repository):
    """Test retrieving an employee by ID successfully."""
    mock_repository.get_by_id.return_value = Employee(
        id=1, name="Jane Doe", email="jane@example.com"
    )

    employee = employee_service.get_employee(1)

    assert employee is not None
    assert employee.id == 1
    assert employee.name == "Jane Doe"


def test_get_employee_not_found(employee_service, mock_repository):
    """Test that retrieving a non-existent employee raises an error."""
    mock_repository.get_by_id.return_value = None

    with pytest.raises(EmployeeNotFound):
        employee_service.get_employee(999)


def test_update_employee_success(employee_service, mock_repository):
    """Test successfully updating an employee."""
    existing_employee = Employee(id=1, name="Old Name", email="test@example.com")
    mock_repository.get_by_id.return_value = existing_employee
    update_data = {"name": "New Name"}

    employee_service.update_employee(1, update_data)

    mock_repository.update.assert_called_once()
    assert existing_employee.name == "New Name"


def test_update_employee_duplicate_email(employee_service, mock_repository):
    """Test updating an employee to an email that already exists raises an error."""
    existing_employee = Employee(id=1, name="Jane Doe", email="jane@example.com")
    conflicting_employee = Employee(id=2, name="John Doe", email="john@example.com")
    mock_repository.get_by_id.return_value = existing_employee
    mock_repository.get_by_email.return_value = conflicting_employee

    update_data = {"email": "john@example.com"}

    with pytest.raises(DuplicateEmailError):
        employee_service.update_employee(1, update_data)

    mock_repository.update.assert_not_called()


def test_delete_employee_success(employee_service, mock_repository):
    """Test successfully deleting an employee."""
    employee_to_delete = Employee(id=1, name="Test User", email="test@example.com")
    mock_repository.get_by_id.return_value = employee_to_delete

    employee_service.delete_employee(1)

    mock_repository.delete.assert_called_once_with(employee_to_delete)


def test_list_employees(employee_service, mock_repository):
    """Test listing all employees."""
    employees_list = [Employee(id=1, name="A"), Employee(id=2, name="B")]
    mock_repository.get_all.return_value = (employees_list, 2)

    employees, total = employee_service.list_employees()

    assert total == 2
    assert len(employees) == 2
    mock_repository.get_all.assert_called_once()

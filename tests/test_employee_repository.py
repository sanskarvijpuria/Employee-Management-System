import pytest

from app.models.employee import Employee
from app.repositories.employee_repository import employee_repository


@pytest.fixture(autouse=True)
def setup_db(client):
    """Fixture to ensure the database is clean for each test in this module."""
    # The client fixture from conftest handles db creation and teardown
    pass


def test_create_employee(client):  # Add client fixture
    """Test creating an employee in the database."""
    emp = Employee(name="Repo User", email="repo@test.com", department="IT", salary=50000)
    created_emp = employee_repository.create(emp)
    assert created_emp.id is not None
    assert created_emp.name == "Repo User"


def test_get_by_id(client):  # Add client fixture
    """Test retrieving an employee by ID."""
    emp = Employee(name="Get User", email="get@test.com")
    created_emp = employee_repository.create(emp)

    found_emp = employee_repository.get_by_id(created_emp.id)
    assert found_emp is not None
    assert found_emp.id == created_emp.id


def test_get_by_email(client):  # Add client fixture
    """Test retrieving an employee by email."""
    emp = Employee(name="Email User", email="email@test.com")
    employee_repository.create(emp)

    found_emp = employee_repository.get_by_email("email@test.com")
    assert found_emp is not None
    assert found_emp.email == "email@test.com"


def test_update_employee(client):  # Add client fixture
    """Test updating an employee's details."""
    emp = Employee(name="Old Name", email="update@test.com")
    created_emp = employee_repository.create(emp)

    created_emp.name = "New Name"
    updated_emp = employee_repository.update(created_emp)

    assert updated_emp.name == "New Name"


def test_delete_employee(client):  # Add client fixture
    """Test deleting an employee."""
    emp = Employee(name="Delete User", email="delete@test.com")
    created_emp = employee_repository.create(emp)
    emp_id = created_emp.id

    employee_repository.delete(created_emp)
    deleted_emp = employee_repository.get_by_id(emp_id)
    assert deleted_emp is None


def test_get_all_with_filters_and_sorting(client):  # Add client fixture
    """Test get_all with filtering, sorting, and pagination."""
    # Setup data
    employee_repository.create(
        Employee(name="Alice", department="HR", salary=60000, email="a@a.com")
    )
    employee_repository.create(
        Employee(name="Bob", department="IT", salary=80000, email="b@b.com")
    )
    employee_repository.create(
        Employee(name="Charlie", department="IT", salary=70000, email="c@c.com")
    )

    # Test department filter
    employees, total = employee_repository.get_all(filters={"department": "IT"})
    assert total == 2
    assert {emp.name for emp in employees} == {"Bob", "Charlie"}

    # Test salary filter
    employees, total = employee_repository.get_all(filters={"min_salary": 75000})
    assert total == 1
    assert employees[0].name == "Bob"

    employees, total = employee_repository.get_all(filters={"max_salary": 65000})
    assert total == 1
    assert employees[0].name == "Alice"

    # Test sorting
    employees, total = employee_repository.get_all(filters={"sort": "salary", "order": "desc"})
    assert total == 3
    assert employees[0].name == "Bob"
    assert employees[2].name == "Alice"

    employees, total = employee_repository.get_all(filters={"sort": "salary", "order": "asc"})
    assert total == 3
    assert employees[0].name == "Alice"
    assert employees[2].name == "Bob"

    # Test pagination
    employees, total = employee_repository.get_all(
        filters={"page": 2, "page_size": 1, "sort": "name"}
    )
    assert total == 3
    assert len(employees) == 1
    assert employees[0].name == "Bob"

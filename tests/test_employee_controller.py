import json

import pytest

from app.extensions import db
from app.models.employee import Employee


@pytest.fixture(autouse=True)
def setup_db(client):
    """Fixture to ensure the database is clean for each test in this module."""
    pass


def test_create_employee_success(client):
    """Test POST /employees - success."""
    response = client.post(
        "/employees/",
        data=json.dumps({"name": "Test User", "email": "test@example.com", "department": "QA"}),
        content_type="application/json",
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"


def test_create_employee_validation_error(client):
    """Test POST /employees - validation error."""
    response = client.post(
        "/employees/",
        data=json.dumps({"name": "Test User", "email": "not-an-email"}),
        content_type="application/json",
    )
    assert response.status_code == 422
    data = response.get_json()
    print("Response Data:", data)
    assert "not-an-email" in data[0]["input"]


def test_create_employee_duplicate_email(client):
    """Test POST /employees - duplicate email error."""
    client.post(
        "/employees/",
        data=json.dumps({"name": "First User", "email": "duplicate@example.com"}),
        content_type="application/json",
    )
    response = client.post(
        "/employees/",
        data=json.dumps({"name": "Second User", "email": "duplicate@example.com"}),
        content_type="application/json",
    )
    assert response.status_code == 409
    data = response.get_json()
    assert "already exists" in data["error"]


def test_get_employee_not_found(client):
    """Test GET /employees/<id> - not found."""
    response = client.get("/employees/999")
    assert response.status_code == 404
    data = response.get_json()
    assert "not found" in data["error"]


def test_get_employee_success(client):
    """Test GET /employees/<id> - success."""
    # Create the employee within the same context as the test client
    emp = Employee(name="Get User", email="get@test.com")
    db.session.add(emp)
    db.session.commit()

    response = client.get(f"/employees/{emp.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == emp.id
    assert data["name"] == "Get User"


def test_get_all_employees(client):
    """Test GET /employees/ - with query params."""
    emp1 = Employee(name="A", email="a@a.com", department="IT")
    emp2 = Employee(name="B", email="b@b.com", department="HR")
    db.session.add_all([emp1, emp2])
    db.session.commit()

    response = client.get("/employees/?department=IT")
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 1
    assert data["employees"][0]["name"] == "A"


def test_update_employee_success(client):
    """Test PUT /employees/<id> - success."""
    emp = Employee(name="Old Name", email="update@test.com")
    db.session.add(emp)
    db.session.commit()

    response = client.put(
        f"/employees/{emp.id}",
        data=json.dumps({"name": "New Name"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "New Name"


def test_update_employee_not_found(client):
    """Test PUT /employees/<id> - not found."""
    response = client.put(
        "/employees/999",
        data=json.dumps({"name": "New Name"}),
        content_type="application/json",
    )
    assert response.status_code == 404


def test_delete_employee_success(client):
    """Test DELETE /employees/<id> - success."""
    emp = Employee(name="Delete Me", email="delete@test.com")
    db.session.add(emp)
    db.session.commit()

    response = client.delete(f"/employees/{emp.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert "deleted successfully" in data["message"]


def test_delete_employee_not_found(client):
    """Test DELETE /employees/<id> - not found."""
    response = client.delete("/employees/999")
    assert response.status_code == 404


def test_generic_exception_handler(client, monkeypatch):
    """Test the generic 500 error handler by forcing the service to raise an exception."""

    def _raise(*args, **kwargs):
        raise Exception("A wild error appeared!")

    # Patch the concrete method used by the controller (list_employees)
    monkeypatch.setattr(
        "app.services.employee_service.employee_service.list_employees",
        _raise,
    )

    response = client.get("/employees/")
    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "InternalServerError"
    assert data["message"] == "A wild error appeared!"

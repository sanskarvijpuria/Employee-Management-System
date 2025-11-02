"""
This module defines the Employee model for the Employee Management System.
The Employee model represents an employee record in the database.
"""

from datetime import datetime

from app.extensions import db


class Employee(db.Model):
    """
    SQLAlchemy model for the employees table.

    Attributes:
        id (int): Primary key.
        name (str): Employee's name.
        email (str): Employee's unique email address.
        department (str): Department name.
        date_joined (datetime): Date the employee joined.
        salary (float): Employee's salary.
    """

    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department = db.Column(db.String(100))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    salary = db.Column(db.Float)

    def __repr__(self) -> str:
        """
        Return a string representation of the Employee instance.

        Returns:
            str: String representation of the employee.
        """
        return f"<Employee {self.name}>"

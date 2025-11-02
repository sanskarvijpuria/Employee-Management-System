"""
This module defines custom exception classes for the Employee Management System.
Each exception represents a specific error condition that can occur in the application.
"""


class EmployeeNotFound(Exception):
    """
    Exception raised when an employee is not found in the database.

    Args:
        message (str): Optional error message.
    """

    def __init__(self, message: str = "Employee not found."):
        super().__init__(message)


class DuplicateEmailError(Exception):
    """
    Exception raised when trying to create an employee with an email that already exists.

    Args:
        message (str): Optional error message.
    """

    def __init__(self, message: str = "Employee with this email already exists."):
        super().__init__(message)

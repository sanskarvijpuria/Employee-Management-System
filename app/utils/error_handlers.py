"""
This module provides error handler registration for the Flask application.
It defines handlers for HTTP, database, validation, and general exceptions.
"""

from flask import jsonify
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from app.exceptions import DuplicateEmailError, EmployeeNotFound


def register_error_handlers(app):
    """
    Register custom error handlers for the Flask app.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        None
    """

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """
        Handle standard HTTP exceptions and return a JSON response.

        Args:
            e (HTTPException): The exception instance.

        Returns:
            Response: JSON response with error details and status code.
        """
        response = {
            "error": e.name,
            "message": e.description,
            "status_code": e.code,
        }
        return jsonify(response), e.code

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e):
        """
        Handle database integrity errors (e.g., constraint violations).

        Args:
            e (IntegrityError): The exception instance.

        Returns:
            Response: JSON response with error message and 409 status.
        """
        return jsonify({"error": "Database integrity error", "message": str(e.orig)}), 409

    @app.errorhandler(EmployeeNotFound)
    def handle_employee_not_found(e):
        """
        Handle EmployeeNotFound exceptions.

        Args:
            e (EmployeeNotFound): The exception instance.

        Returns:
            Response: JSON response with error message and 404 status.
        """
        return jsonify({"error": str(e)}), 404

    @app.errorhandler(DuplicateEmailError)
    def handle_duplicate_email(e):
        """
        Handle DuplicateEmailError exceptions.

        Args:
            e (DuplicateEmailError): The exception instance.

        Returns:
            Response: JSON response with error message and 409 status.
        """
        return jsonify({"error": str(e)}), 409  # 409 Conflict

    @app.errorhandler(ValidationError)
    def handle_pydantic_validation_error(error):
        """
        Handle Pydantic validation errors from flask-pydantic-spec.

        Args:
            error (ValidationError): The validation error instance.

        Returns:
            Response: JSON response with validation error details and 400 status.
        """
        try:
            error_messages = [f"Field '{err['loc'][0]}': {err['msg']}" for err in error.errors()]
            return (
                jsonify({"error": "Validation failed", "details": error_messages}),
                400,
            )
        except (TypeError, KeyError):
            # Fallback for non-standard validation errors
            return jsonify({"error": str(error)}), 400

    @app.errorhandler(Exception)
    def handle_general_exception(e):
        """
        Handle uncaught exceptions and return a generic error response.

        Args:
            e (Exception): The exception instance.

        Returns:
            Response: JSON response with error message and 500 status.
        """
        response = {
            "error": "InternalServerError",
            "message": str(e),
            "status_code": 500,
        }
        return jsonify(response), 500

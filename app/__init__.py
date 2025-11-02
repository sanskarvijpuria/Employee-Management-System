"""
This module initializes the Flask application, configures extensions, middleware, blueprints, error handlers, and API documentation.
It provides the application factory function for the Employee Management System API.
"""

from dotenv import load_dotenv
from flask import Flask

from app.extensions import db, spec
from app.middleware.logging_middleware import setup_request_logging
from app.utils.error_handlers import register_error_handlers

load_dotenv()


def create_app():
    """
    Application factory for the Employee Management System API.

    Initializes Flask app, configures extensions, middleware, blueprints, error handlers, and API docs.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)

    # Register request/response logging middleware
    setup_request_logging(app)

    # Register blueprints
    from app.controllers.employee_controller import employee_bp

    app.register_blueprint(employee_bp, url_prefix="/employees")

    # Register error handlers
    register_error_handlers(app)

    # Configure and register API documentation (Swagger/ReDoc)
    spec.config.TITLE = "Employee Management System API"
    spec.config.VERSION = "1.0.0"
    spec.config.PATH = "docs"
    spec.register(app)

    app.logger.info("Application started successfully.")
    return app

from flask import Flask
from dotenv import load_dotenv
from app.extensions import db
from app.utils.error_handlers import register_error_handlers
import logging
from pythonjsonlogger import jsonlogger
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)

    # Logging setup
    handler = logging.StreamHandler()
    handler.setFormatter(jsonlogger.JsonFormatter())
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    # Register blueprints
    from app.controllers.employee_controller import employee_bp
    app.register_blueprint(employee_bp)

    # Register error handlers
    register_error_handlers(app)

    # DB creation (for demo)
    with app.app_context():
        db.create_all()

    app.logger.info("Application started successfully")
    return app

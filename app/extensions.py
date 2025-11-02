"""
This module initializes and provides shared Flask extensions for the application.
Extensions are instantiated here and imported throughout the app to avoid circular imports.
"""

from flask_pydantic_spec import FlaskPydanticSpec
from flask_sqlalchemy import SQLAlchemy

# API documentation and validation specification
spec = FlaskPydanticSpec("flask")

# SQLAlchemy database instance
db = SQLAlchemy()

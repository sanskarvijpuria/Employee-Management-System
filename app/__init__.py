from flask import Flask
from dotenv import load_dotenv
from app.extensions import db
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    from app.controllers.employee_controller import employee_bp
    app.register_blueprint(employee_bp)

    with app.app_context():
        db.create_all()

    return app

from flask import jsonify
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = {
            "error": e.name,
            "message": e.description,
            "status_code": e.code,
        }
        return jsonify(response), e.code

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e):
        response = {
            "error": "IntegrityError",
            "message": "Database integrity error — likely duplicate or constraint issue.",
            "status_code": 400,
        }
        return jsonify(response), 400

    @app.errorhandler(Exception)
    def handle_general_exception(e):
        response = {
            "error": "InternalServerError",
            "message": str(e),
            "status_code": 500,
        }
        return jsonify(response), 500

"""
This module provides middleware for logging HTTP requests and responses in the Flask application.
It logs request start, finish, status, and duration for observability and debugging.
"""

import time

from flask import g, request


def setup_request_logging(app):
    """
    Register before_request and after_request handlers for logging request and response details.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        None
    """

    @app.before_request
    def start_timer():
        """
        Store the start time and log the beginning of a request.
        """
        g.start_time = time.time()
        app.logger.info(
            "Request started: %s %s from %s", request.method, request.path, request.remote_addr
        )

    @app.after_request
    def log_response(response):
        """
        Log the response status and duration after the request is processed.

        Args:
            response (Response): The Flask response object.

        Returns:
            Response: The unmodified response object.
        """
        if "start_time" in g:
            duration = time.time() - g.start_time
            app.logger.info(
                "Request finished: %s %s with status %s in %.2fs",
                request.method,
                request.path,
                response.status_code,
                duration,
            )
        return response

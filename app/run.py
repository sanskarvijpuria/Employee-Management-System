"""
This module serves as the entry point for running the Flask application.
It also provides a CLI command to initialize the database.
"""

import os

from app import create_app, db

# Create the Flask application instance
app = create_app()


@app.cli.command("init-db")
def init_db_command():
    """
    CLI command to initialize the database tables.

    Usage:
        flask init-db

    Returns:
        None
    """
    with app.app_context():
        db.create_all()
    print("Initialized the database.")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Use 0.0.0.0 to be accessible from outside the container
    app.run(host="0.0.0.0", port=port)

import os

from app import create_app, db

app = create_app()


@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables."""
    with app.app_context():
        db.create_all()
    print("Initialized the database.")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Use 0.0.0.0 to be accessible from outside the container
    app.run(host="0.0.0.0", port=port)

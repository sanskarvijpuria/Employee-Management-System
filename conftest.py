import pytest

from app import create_app, db


@pytest.fixture(scope="session")
def app():
    """
    Create and configure a new app instance for each test session.
    """
    # Use a dedicated testing configuration
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Use in-memory SQLite
            "WTF_CSRF_ENABLED": False,  # Disable CSRF for tests
            "DEBUG": False,
        }
    )
    yield app


@pytest.fixture(scope="function")
def client(app):
    """A test client for the app."""
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

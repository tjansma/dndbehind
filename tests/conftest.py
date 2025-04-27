from flask import Flask
from flask.testing import FlaskClient
import pytest

from dndbehind import create_app, db
from dndbehind.models import User, Role, Background
from config import TestingConfig


@pytest.fixture
def app() -> Flask:
    app = create_app(TestingConfig)
    return app


@pytest.fixture
def db_session(app: Flask):
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def test_user(db_session) -> User:
    user = User(username='testuser', email='test@example.com')
    user.set_password('password123')
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def admin_role(db_session):
    role = Role(name='admin', description='Administrator role')
    db_session.add(role)
    db_session.commit()
    return role


@pytest.fixture
def test_background(db_session):
    background = Background(
        name='Test Background',
        description='A background for testing'
    )
    db_session.add(background)
    db_session.commit()
    return background

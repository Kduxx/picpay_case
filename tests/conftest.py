import pytest
from faker import Faker

from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from picpay_case.models.user import User, Base
from picpay_case.schemas.user import UserCreate
from picpay_case.operations.user import UserOperations

from picpay_case.database import get_db

from fastapi.testclient import TestClient

from picpay_case.main import app


@pytest.fixture(scope="session")
def fake_data():
    return Faker()


@pytest.fixture
def user_factory(fake_data):
    def _create_user_data():
        return dict(
            first_name=fake_data.first_name(),
            last_name=fake_data.last_name(),
            email=fake_data.email(),
            birthdate=fake_data.date_of_birth(),
            phone=fake_data.phone_number()
        )
    return _create_user_data


@pytest.fixture
def test_db() -> Session:
    """Create test session"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # connection fix
        echo=False
    )

    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def api_client(test_db) -> TestClient:
    """
    Fixture for defining a client used by the api tests
    """

    # Override the get_db function to use the fixture for in-memory db
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user_op(test_db) -> UserOperations:
    """
    Fixture for initializing the UserOperations class with the test db
    """
    return UserOperations(test_db)


@pytest.fixture
def existing_user(user_op, user_factory) -> User:
    """Fixture that creates a user for tests that need one"""
    user_data = user_factory()
    return user_op.create_user(UserCreate(**user_data))


@pytest.fixture
def existing_users(user_op, user_factory) -> List[User]:
    """Fixture that creates a user for tests that need one"""
    test_users = [
        user_factory()
        for x in range(5)
    ]

    return [user_op.create_user(UserCreate(**u)) for u in test_users]

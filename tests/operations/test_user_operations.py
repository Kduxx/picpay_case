import pytest
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from picpay_case.operations.user import UserOperations
from picpay_case.models.user import User, Base
from picpay_case.schemas.user import UserCreate


@pytest.fixture
def test_db():
    """
    Fixture for initializing a database for running the tests
    """

    # Uses in-memory sqlite for tests
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )

    session = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    db = session()

    try:
        # Create tables
        try:
            Base.metadata.create_all(bind=engine)
        except Exception as err:
            raise err
        # Yield db session
        yield db
    finally:
        db.close()


@pytest.fixture
def user_op(test_db) -> UserOperations:
    """
    Fixture for initializing the UserOperations class with the test db
    """
    return UserOperations(test_db)


@pytest.fixture
def existing_user(user_op) -> User:
    """Fixture that creates a user for tests that need one"""
    return user_op.create_user(UserCreate(name="Test User"))


@pytest.fixture
def existing_users(user_op) -> List[User]:
    """Fixture that creates a user for tests that need one"""
    mock_users = [
        UserCreate(name="Test User 1"),
        UserCreate(name="Test User 2"),
        UserCreate(name="Test User 3"),
    ]

    created_users = [user_op.create_user(u) for u in mock_users]
    return created_users


def test_create_user(user_op: UserOperations):
    """
    This test validates the user creating by creating a new user;
    Tests the functionality and data integrity after creationg.
    """
    created_user = user_op.create_user(
        user_data=UserCreate(
            name="Jhon Doe"
        )
    )

    assert created_user is not None and isinstance(created_user, User), \
        "create_user function didn't return the created user"

    assert created_user.id is not None, "created user doesn't have an ID"

    # Get the created user from the database to match the info
    db_user = user_op.get_user(created_user.id)

    assert db_user.id == created_user.id, \
        "ID of created user and the retrieved user don't match"
    assert db_user.name == created_user.name, \
        "The name of created user and the retrieved user don't match"


def test_duplicate_user(user_op: UserOperations):
    """
    [PENDING EMAIL FIELD]
    This test validates the creation of duplicate users and expected fails
    """
    pass


def test_get_user(user_op: UserOperations, existing_user: User):
    """
    This test validates that the user info is correctly retrieved
    """
    db_user = user_op.get_user(existing_user.id)
    assert db_user is not None and isinstance(db_user, User), \
        "Data returned from the get_user function is not valid"
    assert db_user.id is not None and db_user.name is not None, \
        "Found null info for non-null fields"


def test_get_non_existing_user(user_op: UserOperations):
    """
    This test validates the request for a non-existing user id
    """
    db_user = user_op.get_user(999)
    assert db_user is None, "Unexpected return when requesting invalid ID"


def test_get_users(user_op: UserOperations, existing_users: List[User]):
    """
    This test adds and selects some mocked users
    """
    db_users = user_op.get_users()
    l_db_users = len(db_users)
    l_e_users = len(existing_users)

    assert l_db_users == l_e_users, \
        "Mismatch in the count of test-created and database-selected users"

    print(f"Databse Users: {db_users} | Total: {l_db_users}")
    print(f"Existing Users: {existing_users} | Total: {l_e_users}")

    assert db_users is not None and isinstance(db_users, List), \
        "Invalid user data received from get_users()"

    db_users_ids = sorted([u.id for u in db_users])
    e_users_ids = sorted([u.id for u in existing_users])

    assert db_users_ids == e_users_ids, \
        "Mismatch in the test-created and database-selected IDs"


def test_update_user(user_op: UserOperations, existing_user: User):
    """
    This test updates a test-created user and validates the update
    """
    new_name = "Updated User Name"

    updated = user_op.update_user(
        user_id=existing_user.id,
        user_data=UserCreate(name=new_name)
    )

    assert updated is not None and isinstance(updated, User), \
        "Invalid user data received from update_user"
    assert updated.name == new_name, \
        "The updated user name doesn't match the requested one"

    db_user = user_op.get_user(existing_user.id)

    assert db_user.name == new_name, \
        "The selected user name doesn't match the updated one"


def test_update_non_existing_user(user_op: UserOperations):
    """
    This test attempts to update a non-existing user and validate it's resposes
    """
    updated = user_op.update_user(999, UserCreate(name="Test"))
    assert updated is None, "Invalid response while updating invalid user"


def test_delete_user(user_op: UserOperations, existing_user: User):
    """
    This test uses a test-created user, deletes it and validates the deletion
    """
    deleted = user_op.delete_user(user_id=existing_user.id)
    assert deleted is True, "User was not properly deleted"

    db_user = user_op.get_user(existing_user.id)
    assert db_user is None, "User still exists in the database after deletion"


def test_delete_non_existing_user(user_op: UserOperations):
    """
    This test validates the delition proccess for a non-existing user
    """
    deleted = user_op.delete_user(user_id=999)
    assert deleted is False, "Invalid response while deleting invalid user"

from typing import List

from picpay_case.operations.user import UserOperations
from picpay_case.models.user import User
from picpay_case.schemas.user import UserCreate, UserUpdate


def test_create_user(user_op: UserOperations, user_factory):
    """
    This test validates the user creating by creating a new user;
    Tests the functionality and data integrity after creationg.
    """
    user_data = user_factory()
    created_user = user_op.create_user(
        user_data=UserCreate(**user_data)
    )

    assert created_user is not None and isinstance(created_user, User), \
        "create_user function didn't return the created user"

    assert created_user.id is not None, "created user doesn't have an ID"

    # Get the created user from the database to match the info
    db_user = user_op.get_user(created_user.id)

    assert db_user.id == created_user.id, \
        "ID of created user and the retrieved user don't match"
    assert db_user.first_name == created_user.first_name, \
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
    assert db_user.id is not None and db_user.first_name is not None, \
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


def test_update_user(user_op: UserOperations, existing_user: User, fake_data):
    """
    This test updates a test-created user and validates the update
    """

    updates = {
        "first_name": fake_data.first_name(),
        "last_name": fake_data.last_name(),
        "email": fake_data.email()
    }

    user_updated = user_op.update_user(
        user_id=existing_user.id,
        user_data=UserUpdate(**updates)
    )

    assert user_updated is not None and isinstance(user_updated, User), \
        "Invalid user data received from update_user"

    def _compare_updates(updates, user):
        for k, v in updates.items():

            assert user.get(k) == updates[k], \
                f"The updated field `{k}` doesn't match the requested one"

    # Compare with the return of the function (updated user)
    _compare_updates(updates, user_updated.to_dict())

    db_user = user_op.get_user(existing_user.id).to_dict()

    # Compare by re-selecting the user from the database
    _compare_updates(updates, db_user)


def test_update_non_existing_user(user_op: UserOperations):
    """
    This test attempts to update a non-existing user and validate it's resposes
    """
    updated = user_op.update_user(999, UserUpdate())
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

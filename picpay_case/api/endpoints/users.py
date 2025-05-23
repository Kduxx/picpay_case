from typing import List

from fastapi import APIRouter
from fastapi import Depends
from picpay_case.schemas.user import UserResponse, UserCreate
from picpay_case.operations.user import UserOperations
from picpay_case.api.deps import get_user_operations

from picpay_case.schemas.response import (
    success_response,
    fail_response,
    error_response
)

router = APIRouter(prefix="/users")


@router.get("/", response_model=List[UserResponse])
def list_users(
    user_op: UserOperations = Depends(get_user_operations)
):
    users = user_op.get_users()
    return users


@router.get("/{user_id}")
def get_user(
    user_id: int,
    user_op: UserOperations = Depends(get_user_operations)
):
    try:
        user = user_op.get_user(user_id)
        if not user:
            return fail_response(f"User with ID '{user_id}' not found")
        user_response = UserResponse.model_validate(user)
        return success_response(user_response)
    except Exception as err:
        print(err)  # Replace with logging
        return error_response()


@router.post("/")
def add_user(
    user_data: UserCreate,
    user_op: UserOperations = Depends(get_user_operations)
):
    try:
        user = user_op.create_user(user_data)
        user_response = UserResponse.model_validate(user)
        return success_response(
            data=user_response,
            message=f"User {user.name} created with id {user.id}"
            )
    except Exception as err:
        print(err)
        return error_response()


@router.put("/{user_id}")
def update_user(
    user_id: int,
    user_data: UserCreate,
    user_op: UserOperations = Depends(get_user_operations)
):
    try:
        user = user_op.update_user(user_id, user_data)
        if not user:
            return fail_response(f"User #{user_id} was not found")
        user_response = UserResponse.model_validate(user)
        return success_response(
            data=user_response,
            message=f"User #{user.id} ({user.name}) Updated"
        )
    except Exception as err:
        print(err)
        return error_response()


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    user_op: UserOperations = Depends(get_user_operations)
):
    try:
        is_deleted = user_op.delete_user(user_id)
        if not is_deleted:
            return fail_response(f"User #{user_id} could not be deleted")
        return success_response(
            data={'deleted': is_deleted},
            message=f"User #{user_id} deleted successfully"
        )
    except Exception as err:
        print(err)
        return error_response()

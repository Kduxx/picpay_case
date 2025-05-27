from fastapi import APIRouter, Depends, status, HTTPException
from picpay_case.schemas.user import UserResponse, UserCreate, UserUpdate
from picpay_case.operations.user import UserOperations
from picpay_case.api.deps import get_user_operations

from picpay_case.schemas.response import (
    success_response
)

router = APIRouter(prefix="/users")


@router.get("/")
def list_users(
    user_op: UserOperations = Depends(get_user_operations)
):
    """
    Endpoint for listing all of the users in the database
    """
    users = user_op.get_users()
    user_response = [UserResponse.model_validate(u) for u in users]
    return success_response(user_response)


@router.get("/{user_id}")
def get_user(
    user_id: int,
    user_op: UserOperations = Depends(get_user_operations)
):
    """
    Endoint for retrieving information for a single user based on the ID
    """
    user = user_op.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User  #{user_id} not found"
        )
    user_response = UserResponse.model_validate(user)
    return success_response(user_response)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_user(
    user_data: UserCreate,
    user_op: UserOperations = Depends(get_user_operations)
):
    """
    Endpoint for adding a new user to the database
    """
    user = user_op.create_user(user_data)
    user_response = UserResponse.model_validate(user)
    return success_response(
        data=user_response,
        message=f"User {user.email} created with id {user.id}"
        )


@router.put("/{user_id}")
def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_op: UserOperations = Depends(get_user_operations)
):
    """
    Endpoing for updating a user in the database with the their ID
    """
    user = user_op.update_user(user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User #{user_id} not found"
        )
    user_response = UserResponse.model_validate(user)
    return success_response(
        data=user_response,
        message=f"User #{user.id} ({user.email}) Updated"
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    user_op: UserOperations = Depends(get_user_operations)
):
    """
    Endpoint for deleting a user from the database based on their ID
    """
    is_deleted = user_op.delete_user(user_id)
    if not is_deleted:
        raise HTTPException(
            status_code=404, detail=f"User #{user_id} not found"
        )

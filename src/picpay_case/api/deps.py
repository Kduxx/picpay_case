from fastapi import Depends
from sqlalchemy.orm import Session
from picpay_case.database import get_db
from picpay_case.operations.user import UserOperations


def get_user_operations(db: Session = Depends(get_db)):
    """
    Manage dependencies to get and instance of UserCRUD
    """
    return UserOperations(db)

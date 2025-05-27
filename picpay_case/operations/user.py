from typing import List, Optional
from sqlalchemy.orm import Session
from picpay_case.models.user import User
from picpay_case.schemas.user import UserCreate, UserUpdate


class UserOperations:
    """
    Encapsulates operations for User entity
    """

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:

        user_d = user_data.model_dump()
        create_user = User(**user_d)

        self.db.add(create_user)
        self.db.commit()
        self.db.refresh(create_user)

        return create_user

    def get_user(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_users(self) -> List[User]:
        return self.db.query(User).all()

    def update_user(
            self,
            user_id: int,
            user_data: UserUpdate
    ) -> Optional[User]:
        db_user = self.get_user(user_id)
        if not db_user:
            return None

        # Dump model as a dictionary excluding null columns
        update_data = user_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_user, field, value)

        # Commit changes and reload user info
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def delete_user(
        self,
        user_id: str
    ) -> bool:
        db_user = self.get_user(user_id)
        if not db_user:
            return False

        self.db.delete(db_user)
        self.db.commit()

        return True

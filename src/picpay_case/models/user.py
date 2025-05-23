from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from picpay_case.database import Base


class User(Base):
    """
    User model
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id})>"

    def __str__(self) -> str:
        return f"User #{self.id}: {self.name}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }

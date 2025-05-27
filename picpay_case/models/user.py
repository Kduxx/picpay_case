from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, DateTime
from picpay_case.database import Base
from datetime import datetime, date


class User(Base):
    """
    User model
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(320), nullable=False)

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    birthdate: Mapped[date] = mapped_column(Date, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, onupdate=datetime.utcnow,
        default=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id})>"

    def __str__(self) -> str:
        full_name = f"{self.first_name} {self.last_name}"
        return f"User #{self.id}: {full_name}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "birthdate": self.birthdate,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

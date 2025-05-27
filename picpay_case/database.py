from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from picpay_case.core.config import settings


engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


# Base ORM class used by other classes to add definitions to
class Base(DeclarativeBase):
    pass


def create_database_tables():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as err:
        raise err


def get_db():
    db = SessionLocal()
    try:
        create_database_tables()
        yield db
    finally:
        db.close()

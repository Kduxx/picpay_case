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


class Base(DeclarativeBase):
    pass


def create_database_tables():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as err:
        raise err


def init_db():
    create_database_tables()


def get_db():
    db = SessionLocal()
    try:
        init_db()
        yield db
    finally:
        db.close()

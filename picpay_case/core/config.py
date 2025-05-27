import os


class Settings:
    database_url: str = os.environ.get("DB_URL", "sqlite:///.db.sqlite")


settings = Settings()

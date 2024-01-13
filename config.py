import os
from dotenv import load_dotenv


class Settings:
    app_name: str = "My API"
    db_password: str = ""
    db_user: str = "postgres"
    db_name: str = "postgres"
    db_host: str = "localhost"
    db_driver: str = ""

    def build_db_url(self):
        return f"postgresql{self.db_driver}://" \
               f"{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"


load_dotenv()
settings = Settings()
settings.db_password = os.environ.get("DB_PASSWORD")
settings.db_name = os.environ.get("DB_NAME")
settings.db_user = os.environ.get("DB_USER")
settings.db_host = os.environ.get("DB_HOST")
settings.db_driver = os.environ.get("DB_DRIVER")

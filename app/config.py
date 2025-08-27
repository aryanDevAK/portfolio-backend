import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./portfolio.db"
    api_key: str = "your_secret_api_key"
    admin_email: str = "admin@example.com"
    admin_password: str = "yourpassword"
    
    mail_username: str = ""
    mail_password: str = ""
    mail_from: str = ""
    mail_port: int = 587
    mail_server: str = "smtp.gmail.com"
    
    class Config:
        env_file = ".env"

settings = Settings()

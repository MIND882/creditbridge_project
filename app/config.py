from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/.env ka absolute path
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"



class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        extra="ignore",
    )

    # App
    APP_ENV: str = "development"
    APP_BASE_URL: str = "http://localhost:8000"
    @property
    def is_development(self) -> bool:
        return self.APP_ENV.lower() == "development"

    SECRET_KEY: str

    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 15
    JWT_REFRESH_EXPIRATION_DAYS: int = 7

    # Database
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379"

    # Razorpay
    RAZORPAY_KEY_ID: Optional[str] = None
    RAZORPAY_KEY_SECRET: Optional[str] = None
    RAZORPAY_WEBHOOK_SECRET: Optional[str] = None

    # Surepass
    SUREPASS_API_TOKEN: Optional[str] = None
    SUREPASS_BASE_URL: str = "https://sandbox.surepass.io"

    # Setu
    SETU_CLIENT_ID: Optional[str] = None
    SETU_CLIENT_SECRET: Optional[str] = None
    SETU_PRODUCT_INSTANCE_ID: Optional[str] = None
    SETU_BASE_URL: str = "https://fiu-sandbox.setu.co"
    SETU_WEBHOOK_URL: Optional[str] = None

    # GST
    GSTN_API_KEY: Optional[str] = None
    GSTN_BASE_URL: str = "https://api.gstn.org.in"

    # AI
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    OPEN_API_KEY: Optional[str] = None
    ENCRYPTION_KEY: str = "your-encryption-key"

    # Twilio
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None
    TWILIO_WHATSAPP_FROM: Optional[str] = None


settings = Settings()


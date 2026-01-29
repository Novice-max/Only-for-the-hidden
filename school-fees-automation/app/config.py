from pydantic import BaseSettings

class Settings(BaseSettings):
    mpesa_consumer_key: str = ""
    mpesa_consumer_secret: str = ""
    callback_url: str = ""

settings = Settings()

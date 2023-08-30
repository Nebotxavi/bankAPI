from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    password: str = ""
    db_username: str = ""
    port: int = 0

    db_name: str = ""
    db_type: str = ""

    secret_key: str = ""
    algorithm: str = ""
    access_token_expire_minutes: int = 0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class DbConfig(BaseModel):
    password: str = ""
    db_username: str = ""
    port: int = 0

    db_name: str = ""
    db_type: str = ""


class Settings(BaseModel):
    secret_key: str = ""
    algorithm: str = ""
    access_token_expire_minutes: int = 0


config = Config()

dbConfig = DbConfig.model_validate(config.model_dump())
settings = Settings.model_validate(config.model_dump())

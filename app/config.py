from pydantic import BaseSettings

class DbConfig(BaseSettings):
    postgresql_hostname: str = ''
    postgresql_port: str = '' 
    postgresql_password: str = ''
    postgresql_username: str = ''

    mongo_password: str = ''
    mongo_username: str = ''   

    db_name: str = ''
    db_type: str = ''

    # secret_key: str
    # algorithm: str
    # access_token_expire_minutes: int

    class Config:
        env_file = '.env'


dbConfig = DbConfig() # pyright: ignore
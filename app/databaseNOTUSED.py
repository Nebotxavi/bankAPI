from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import dbConfig

# TODO: to be removed

SQLALCHEMY_DATABASE_URL = f'postgresql://{dbConfig.postgresql_username}:{dbConfig.postgresql_password}@{dbConfig.postgresql_hostname}:{dbConfig.postgresql_port}/{dbConfig.db_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
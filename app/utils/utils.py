import datetime
from passlib.context import CryptContext


class IdGenerator:
    @staticmethod
    def get_id() -> int:
        return int(datetime.datetime.now().timestamp()*100000)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Crypt:

    @staticmethod
    def hash(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def verify(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import cursor


from ..config import DbConfig
from typing import List, Any


# TODO: switch to SQL alchemy (engine, session_local, base...)
# TODO: decorator for opening/closing the DB

def test_decorator(func):
    def wrapper(self, *args):
        print('connect')
        conn = psycopg2.connect(
                host=self.host, 
                database=self.database, 
                user=self.user,
                password=self.password, 
                cursor_factory=RealDictCursor)
        self.client = conn.cursor()

        test = func(self, *args)
        print('close')
        self.client.close()

        return test
    return wrapper

class PostgresStorage:
    client: cursor

    def __init__(self, dbConfig: DbConfig) -> None:

            self.host=dbConfig.postgresql_hostname
            self.database=dbConfig.db_name
            self.user=dbConfig.postgresql_username
            self.password=dbConfig.postgresql_password

            # conn = psycopg2.connect(
            #     host=dbConfig.postgresql_hostname, 
            #     database=dbConfig.db_name, 
            #     user=dbConfig.postgresql_username,
            #     password=dbConfig.postgresql_password, 
            #     cursor_factory=RealDictCursor )
            # self.client = conn.cursor()

    # TODO: fix types (avoid any)
    @test_decorator
    def test_database(self) -> List[Any]:
        print('execute')
        self.client.execute(''' SELECT * FROM health ''')
        return self.client.fetchall()

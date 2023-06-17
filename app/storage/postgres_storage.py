import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import cursor
from typing import List, Any

from ..config import DbConfig
from ..models.products import Product
from ..models.customers import Customer, CustomerIn

# TODO: switch to SQL alchemy (engine, session_local, base...)


def handle_db_connection(func):
    def wrapper(self, *args):
        conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            cursor_factory=RealDictCursor)
        self.client = conn.cursor()

        func_with_client = func(self, *args)
        self.client.close()

        return func_with_client
    return wrapper


class PostgresStorage:
    client: cursor

    def __init__(self, dbConfig: DbConfig) -> None:
        self.host = dbConfig.postgresql_hostname
        self.database = dbConfig.db_name
        self.user = dbConfig.postgresql_username
        self.password = dbConfig.postgresql_password

    @handle_db_connection
    def test_database(self) -> List[Any]:  # TODO: fix types (avoid any)
        self.client.execute(''' SELECT * FROM health ''')
        return self.client.fetchall()

    def get_products_list(self) -> List[Product]:
        ...

    def get_product(self, id) -> Product:
        ...

    def get_customers_list(self) -> List[Customer]:
        ...

    def get_customer(self, id: int) -> Customer:
        ...

    def create_customer(self, customer: CustomerIn) -> Customer:
        ...

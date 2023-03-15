import psycopg2
from src.config import DB_HOST, DB_NAME, DB_USER, DB_PWD


class PostgresClient:
    db_client = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PWD
    )

    def get_cursor(self):
        return self.db_client.cursor()
from sqlalchemy import create_engine
from src.config import DB_HOST, DB_NAME, DB_USER, DB_PWD, PORT


class PostgresClient:

    db_engine=create_engine(f"postgresql://{DB_USER}:{DB_PWD}@{DB_HOST}:{PORT}/{DB_NAME}")


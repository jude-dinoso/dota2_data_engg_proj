import io
from enum import Enum

from pandas import DataFrame
from sqlalchemy import create_engine
from src.config import DB_HOST, DB_NAME, DB_USER, DB_PWD, PORT


class TableOperation(str, Enum):
    APPEND = "append"
    REPLACE = "replace"


class PostgresClient:

    engine = create_engine(f"postgresql://{DB_USER}:{DB_PWD}@{DB_HOST}:{PORT}/{DB_NAME}")
    conn = engine.connect()
    raw_conn = engine.raw_connection()

    def _create_table(self, df: DataFrame, table_name: str, operation: TableOperation):
        try:
            if_exists = "replace" if operation == TableOperation.REPLACE else "fail"
            df.head(0).to_sql(table_name, self.engine, if_exists=if_exists, index=False)
        except Exception:
            print(f"Table {table_name} already exists")

    def insert_data(self, data_df: DataFrame, table_name: str, operation: TableOperation):
        self._create_table(data_df, table_name, operation)
        cur = self.raw_conn.cursor()
        output = io.StringIO()
        data_df.to_csv(path_or_buf=output, sep='\t', header=False, index=False)
        output.seek(0)
        cur.copy_from(output, "table_name", null="")  # null values become ''
        cur.close()
        self.conn.commit()

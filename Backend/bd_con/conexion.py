import psycopg2 as pg
from dotenv import load_dotenv
import os

load_dotenv()


class PsqlConnection:
    def __init__(self):
        DB_NAME = os.environ.get("DEV_DB_NAME") if os.environ.get("ENV") == 'dev' else os.environ.get("DB_NAME")

        try:
            self.conn = pg.connect(
                dbname=DB_NAME,
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                host=os.environ.get("DB_HOSTNAME"),
                port=int(os.environ.get("DB_PORT")),
            )
        except Exception as e:
            raise ConnectionError('Connection not reached, check your credentials')




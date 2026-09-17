import psycopg2
from dotenv import load_dotenv
import os


def connexion():
    load_dotenv()

    connection = psycopg2.connect(
        host="postgres",
        database=os.getenv("ELT_DATABASE_NAME"),
        user=os.getenv("POSTGRES_CONN_USERNAME"),
        password=os.getenv("POSTGRES_CONN_PASSWORD"),
        port="5432"
    )

    return connection
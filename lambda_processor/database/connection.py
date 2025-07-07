import os
import psycopg2


def get_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        dbname=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        port=int(os.environ.get('DB_PORT', 5432)),
    )

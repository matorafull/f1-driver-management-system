import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="f1_racing_db",
        user="postgres",
        password="dexter553",            # Поменяйте пароль
        cursor_factory=RealDictCursor
    )
    return conn


def execute_query(query, params=None, fetch=False):
    conn = get_db_connection()
    if conn is None: return None

    cur = conn.cursor()
    cur.execute(query, params)

    result = None
    if fetch:
        result = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()
    return result
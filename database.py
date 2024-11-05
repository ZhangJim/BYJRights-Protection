import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="your_database_name",
            user="your_username",
            password="your_password",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        raise 
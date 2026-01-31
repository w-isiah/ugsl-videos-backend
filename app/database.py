"""
Simple database connection
"""
import pymysql
import pymysql.cursors
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

@contextmanager
def get_db():
    """Get database connection"""
    conn = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'ugsl_db_1'),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )
    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def get_cursor():
    """Get database cursor with auto commit/rollback"""
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

def test_connection():
    """Test database connection"""
    try:
        with get_cursor() as cursor:
            cursor.execute("SELECT 1")
            return True
    except:
        return False
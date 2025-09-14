import sqlite3
import functools

def with_db_connection(func):
    """Decorator that automatically handles opening and closing database connections"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        except Exception as e:
            raise e
        finally:
            conn.close()
    return wrapper

def transactional(func):
    """Decorator that ensures database operations are wrapped in a transaction"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        original_autocommit = conn.isolation_level
        savepoint_name = None
        try:
            if conn.isolation_level is None:
                conn.isolation_level = 'DEFERRED'
            else:
                savepoint_name = f"sp_{id(conn)}_{id(func)}"
                conn.execute(f"SAVEPOINT {savepoint_name}")

            result = func(conn, *args, **kwargs)

            if savepoint_name:
                conn.execute(f"RELEASE SAVEPOINT {savepoint_name}")
            else:
                conn.isolation_level = original_autocommit
            return result

        except Exception as e:
            if savepoint_name:
                conn.execute(f"ROLLBACK TO SAVEPOINT {savepoint_name}")
            else:
                conn.isolation_level = original_autocommit
            raise e

    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?",
                   (new_email, user_id))

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')

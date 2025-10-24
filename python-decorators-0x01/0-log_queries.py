import sqlite3
import functools
from datetime import datetime




def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            arg = args[0]
        else:
            arg = kwargs.get("query")
        print(f"[{datetime.now()}] Executing SQL query: {arg}")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


users = fetch_all_users(query="SELECT * FROM users")

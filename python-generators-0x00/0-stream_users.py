#!/usr/bin/python3
"""
0-stream_users.py
Generator function that streams rows from user_data one by one.
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Generator that yields rows from user_data table as dictionaries.
    Uses only one loop.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",       # change if needed
            password="",       # supply password if needed
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        for row in cursor:
            # row is already a dictionary since dictionary=True
            yield row

    except Error as e:
        print(f"Error streaming users: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

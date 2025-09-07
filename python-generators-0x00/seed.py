#!/usr/bin/python3
"""
seed.py – setup script for MySQL database ALX_prodev and user_data table.
"""

import mysql.connector
from mysql.connector import Error
import uuid
import csv


def connect_db():
    """
    Connect to MySQL server (not a specific database).
    Returns connection object or None.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",       # change if different user
            password=""        # supply password if needed
        )
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


def create_database(connection):
    """
    Create database ALX_prodev if it does not exist.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """
    Connect directly to ALX_prodev database.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        return connection
    except Error as e:
        print(f"Error while connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """
    Create table user_data if it does not exist.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            );
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """
    Insert rows from CSV into user_data table.
    Each row is inserted only if user_id not already present.
    """
    try:
        cursor = connection.cursor()

        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # If CSV does not have user_id, generate UUID
                user_id = row.get("user_id") or str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = row["age"]

                # Insert only if not already present
                cursor.execute("""
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, name, email, age))

        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"CSV file {csv_file} not found")

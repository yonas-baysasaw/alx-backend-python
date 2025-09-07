#!/usr/bin/python3

import mysql.connector


def stream_users():

    try:
        # Connect directly to ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # update if using another MySQL user
            password="root",      # update with your MySQL password
            database="ALX_prodev"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data;")

        # Yield rows one by one
        for row in cursor:
            yield row

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

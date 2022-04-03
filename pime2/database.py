import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        print("Successfully connected to database", db_file)
        return connection

    except Error as e:
        print("An error occured while connecting to the database:")
        print(e)


def disconnect(connection):
    if connection:
        connection.close()
        print("Successfully disconnected from the database")


def create_default_tables(connection, cursor):
    sql_create_sensors_table = """CREATE TABLE IF NOT EXISTS sensors (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL );"""

    try:
        cursor.execute(sql_create_sensors_table)
        connection.commit()
        print("Successfully created all default tables")
    except Error as e:
        print(e)



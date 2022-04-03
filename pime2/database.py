import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """
    This method creates a database if none exists and establishes a connection to it
    :param db_file: file path to the database
    :return: connection
    """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print("Successfully connected to database", db_file)
    except Error as err:
        print("An error occurred while connecting to the database:")
        print(err)

    return connection


def disconnect(connection):
    """
    This method disconnects from the database
    :param connection: connection to the database
    :return:
    """
    if connection:
        connection.close()
        print("Successfully disconnected from the database")


def create_default_tables(connection, cursor):
    """
    This method creates all mandatory tables
    :param connection: connection to the database
    :param cursor: cursor for the database
    :return:
    """
    sql_create_sensors_table = """CREATE TABLE IF NOT EXISTS sensors (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL );"""

    try:
        cursor.execute(sql_create_sensors_table)
        connection.commit()
        cursor.close()
        print("Successfully created all default tables")
    except Error as err:
        print(err)

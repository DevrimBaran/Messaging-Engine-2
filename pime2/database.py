import sys
import sqlite3
import logging
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
        logging.info("Successfully connected to database: %s", db_file)
    except Error:
        logging.exception("An error occurred while connecting to the database. \n Pime will now shutdown safely.")
        sys.exit(1)
    return connection


def disconnect(connection):
    """
    This method disconnects from the database
    :param connection: connection to the database
    :return:
    """
    if connection:
        connection.close()
        logging.info("Successfully disconnected from the database")


def create_default_tables(connection):
    """
    This method creates all mandatory tables
    :param connection: connection to the database
    :return:
    """
    sql_create_sensors_table = """CREATE TABLE IF NOT EXISTS sensors (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL );"""

    cursor = connection.cursor()
    try:
        cursor.execute(sql_create_sensors_table)
        connection.commit()
        logging.info("Successfully created all default tables")
    except Error:
        logging.exception("An error occurred while creating the default tables")
    finally:
        cursor.close()

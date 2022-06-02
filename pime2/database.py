import sys
import sqlite3
import logging
from sqlite3 import Error, Connection

DB_CONNECTION: Connection
from pime2.entity import NodeEntity
from pime2.service.node_service import NodeService
from pime2.config import get_me_conf



def create_connection(db_file):
    """
    This method creates a database if none exists and establishes a connection to it
    :param db_file: file path to the database
    :return: connection
    """
    # pylint: disable=global-statement
    global DB_CONNECTION
    connection = None
    try:
        DB_CONNECTION = sqlite3.connect(db_file)
        connection = DB_CONNECTION
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
    sql_create_nodes_table = """CREATE TABLE IF NOT EXISTS nodes (
                                    id integer PRIMARY KEY,
                                    name varchar(255) NOT NULL UNIQUE,
                                    ip varchar(255) NOT NULL,
                                    port int NOT NULL,
                                    sensor_skills varchar(255),
                                    actuator_skills varchar(255));"""

    own_node = NodeEntity(name=get_me_conf().instance_id, ip=get_me_conf().host, port=get_me_conf().port)
    service = NodeService()

    cursor = connection.cursor()
    try:
        cursor.execute(sql_create_nodes_table)
        connection.commit()
        logging.info("Successfully created all default tables")
        service.put_node(own_node)
    except Error:
        logging.exception("An error occurred while creating the default tables")
    finally:
        cursor.close()


def get_db_connection():
    """
    Returns an instance of the database
    :return:
    """
    return DB_CONNECTION

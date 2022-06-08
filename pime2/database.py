import sys
import sqlite3
import logging
from sqlite3 import Error, Connection

from pime2.entity import NodeEntity
from pime2.config import get_me_conf

DB_CONNECTION: Connection


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


def create_default_tables(connection, node_service):
    """
    This method creates all mandatory tables
    :param node_service: NodeService
    :param connection: connection to the database
    :return:
    """
    sql_create_nodes_table = """CREATE TABLE IF NOT EXISTS nodes (
                                    id integer PRIMARY KEY,
                                    name varchar(255) NOT NULL UNIQUE,
                                    ip varchar(60) NOT NULL,
                                    port int NOT NULL,
                                    sensor_skills varchar(255),
                                    actuator_skills varchar(255));"""

    cursor = connection.cursor()
    try:
        cursor.execute(sql_create_nodes_table)
        connection.commit()
        logging.info("Successfully created all default tables")
        create_own_node(node_service)
    except Error:
        logging.exception("An error occurred while creating the default tables")
    finally:
        cursor.close()

def create_own_node(node_service):
    """
    This method creates the own device node
    :param node_service: NodeService
    :return:
    """
    own_me_node = node_service.get_own_node()
    if own_me_node is None:
        logging.info("Own node not existing. Creating own node.")
        conf = get_me_conf()
        sensor_skills = []
        actuator_skills = []
        try:
            for sensor in conf.available_sensors():
                sensor_skills.append(sensor.name)
            logging.info("Loading sensors.")
            for actuator in conf.available_actuators():
                actuator_skills.append(actuator.name)
            logging.info("Loading actuators.")
        except RuntimeError as err:
            logging.error("Faulty configuration. Error: <%s>", err)
        finally:
            own_me_node = NodeEntity(conf.instance_id, conf.host, conf.port,sensor_skills,actuator_skills)
            node_service.put_node(own_me_node)
            logging.info("Created own node successfully!")
    else:
        node_service.put_node(own_me_node)
        logging.info("Created own node successfully!")

def get_db_connection():
    """
    Returns an instance of the database
    :return:
    """
    return DB_CONNECTION

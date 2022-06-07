# pylint: disable=C0301
import logging
import sqlite3
from sqlite3 import IntegrityError
from typing import List, Optional

from pime2.entity import NodeEntity
from pime2.config import get_me_conf


class NodeRepository:
    """Implements node repository class"""

    def __init__(self, connection):
        self.connection = connection

    def create_node(self, node: NodeEntity):
        """Saves a node in database"""
        cursor = self.connection.cursor()

        # delete a node with an existing name like this to avoid old data
        if self.check_in_database(node.name):
            self.delete_node_by_name(node.name)

        query = 'INSERT INTO nodes(name,ip,port,sensor_skills,actuator_skills) VALUES(?,?,?,?,?);'
        logging.debug('Executing SQL query: "%s"', query)
        logging.debug('Values inserted: name:<%s> ip:<%s> port:<%s> sensor_skills:<%s> actuator_skills: <%s>',
                      node.name, node.ip, node.port, node.sensor_skills, node.actuator_skills)
        try:
            cursor.execute(query, (
                node.name, node.ip, node.port, ",".join(node.sensor_skills), ",".join(node.actuator_skills),))
            self.commit()
        except IntegrityError:
            logging.debug("Integrity error during insert detected")
        finally:
            cursor.close()

    def read_node_by_name(self, name: str) -> Optional[NodeEntity]:
        """Return a node with a specific name from database"""
        cursor = self.connection.cursor()
        query = 'SELECT * FROM nodes WHERE name = ?;'
        logging.debug('Executing SELECT SQL query: "%s" with name:<%s>', query, name)

        try:
            cursor.execute(query, (name,))
            node_in_database = cursor.fetchone()
            if node_in_database is None:
                logging.debug('No node with name "%s" exists.', name)
                return None
            logging.debug('Query executed. Result: %s', node_in_database)
            result_node = NodeEntity(node_in_database[1], node_in_database[2], node_in_database[3],
                                     str(node_in_database[4]).split(","), str(node_in_database[5]).split(","))

            return result_node
        finally:
            cursor.close()

    def read_all_nodes(self) -> List[NodeEntity]:
        """Return every node in the database as a list"""
        cursor = self.connection.cursor()
        query = 'SELECT * FROM nodes;'
        logging.debug('Executing SELECT SQL query: "%s"', query)

        try:
            cursor.execute(query)
            nodes_in_database = cursor.fetchall()
            if len(nodes_in_database) == 0 or nodes_in_database is None:
                logging.debug('No nodes existing.')
                return []
            logging.debug('Query executed. Result: %s', nodes_in_database)
            result_list = []
            for node in nodes_in_database:
                sensor_skills = [] if list(node[4]).__len__() == 0 else node[4].split(",")
                actuator_skills = [] if list(node[5]).__len__() == 0 else node[5].split(",")
                result_list.append(NodeEntity(node[1], node[2], node[3], sensor_skills, actuator_skills))
            return result_list
        finally:
            cursor.close()

    def update_node(self, node: NodeEntity):
        """Updates a specific node"""
        cursor = self.connection.cursor()
        query = """
        UPDATE nodes
        SET ip = ?, port = ?, sensor_skills = ?, actuator_skills = ?
        WHERE name = ?; 
        """
        try:
            if self.check_in_database(node.name):
                logging.debug('Current node: <%s>', node)
                logging.debug('Executing UPDATE SQL query: "%s"', query)
                logging.debug('Updating values to: ip:<%s> port:<%s> sensor_skills:<%s> actuator_skills: <%s>', node.ip,
                              node.port, node.sensor_skills, node.actuator_skills)
                cursor.execute(query, (
                    node.ip, node.port, ",".join(node.sensor_skills), ",".join(node.actuator_skills), node.name))
                self.commit()
                logging.debug('Updated record.')
            else:
                logging.debug('Can not update non existing node with name "%s".', node.name)
                raise sqlite3.Error("Can not update non existing node")
        finally:
            cursor.close()

    def delete_node_by_name(self, name: str):
        """Deletes a specific node by its name"""
        cursor = self.connection.cursor()
        if self.check_in_database(name):
            query = 'DELETE FROM nodes WHERE name = ?;'
            logging.debug('Executing DELETE SQL query: "%s" with name:<%s>.', query, name)
            cursor.execute(query, (name,))
            self.commit()
            logging.debug('Deleted record with name "%s".', name)
            cursor.close()
        else:
            logging.debug('Can not delete non existing node with name "%s".', name)
            raise sqlite3.Error("Can not delete non existing node")

    def delete_all(self):
        """Deletes the node records of the node table"""
        cursor = self.connection.cursor()
        query = 'DELETE FROM nodes;'
        logging.debug('Executing DELETE ALL SQL query: "%s"', query)
        cursor.execute(query)
        self.commit()
        logging.debug('Deleted all records from table "node"')
        cursor.close()

    def commit(self):
        """Commits the database transactions"""
        self.connection.commit()

    def check_in_database(self, name: str) -> bool:
        """Checks if a node with a specific name is in database"""
        return self.read_node_by_name(name) is not None

    def read_all_neighbors(self) -> List[NodeEntity]:
        """Return every node except the own device node from the database as a list"""
        cursor = self.connection.cursor()
        query = 'SELECT * FROM nodes WHERE name != ?;'
        logging.debug('Executing SELECT SQL query: "%s"', query)
        cursor.execute(query, (get_me_conf().instance_id,))
        try:
            neighbors = cursor.fetchall()
            if neighbors is None:
                logging.debug('No nodes existing.')
                return None
            logging.debug('Query executed. Result: %s', neighbors)
        finally:
            cursor.close()
        result_list = []
        for node in neighbors:
            result_list.append(NodeEntity(node[1], node[2], node[3], node[4], node[5]))
        return result_list

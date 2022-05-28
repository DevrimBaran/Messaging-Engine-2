# pylint: disable=C0301
import logging
import sqlite3
from sqlite3 import IntegrityError
import pime2.database as db
from pime2.entity.node import NodeEntity


class NodeRepository():
    """Implements node repository class"""

    def __init__(self):
        self.connection = db.create_connection("pime_database.db")

    def create_node(self, node : NodeEntity):
        """Saves a node in database"""
        cursor = self.connection.cursor()
        query = 'INSERT INTO nodes(name,ip,port) VALUES(?,?,?);'
        logging.debug('Executing SQL query: "%s"', query)
        logging.debug('Values inserted: name:<%s> ip:<%s> port:<%s>', node.name, node.ip, node.port)
        try:
            cursor.execute(query, (node.name, node.ip, node.port))
        except IntegrityError as integrity_err:
            logging.debug('Node with name "%s" exists already. Please only give unique names. Error: %s', node.name, integrity_err)
            raise IntegrityError("Duplicate Entry") from integrity_err
        finally:
            self.commit()
            cursor.close()

    def read_node_by_name(self, name : str) -> NodeEntity:
        """Return a node with a specific name from database"""
        cursor = self.connection.cursor()
        query = 'SELECT * FROM nodes WHERE name = ?;'
        logging.debug('Executing SELECT SQL query: "%s" with name:<%s>', query, name)
        cursor.execute(query, (name,))
        node_in_database = cursor.fetchone()
        if node_in_database is None:
            logging.debug('No node with name "%s" exists.', name)
            return None
        logging.debug('Query executed. Result: %s', node_in_database)
        result_node = NodeEntity(node_in_database[1],node_in_database[2],node_in_database[3])
        cursor.close()
        return result_node

    def read_all_nodes(self) -> list[NodeEntity]:
        """Return every node in the database as a list"""
        cursor = self.connection.cursor()
        query = 'SELECT * FROM nodes;'
        logging.debug('Executing SELECT SQL query: "%s"', query)
        cursor.execute(query)
        nodes_in_database = cursor.fetchall()
        if nodes_in_database is None:
            logging.debug('No nodes existing.')
            return None
        logging.debug('Query executed. Result: %s', nodes_in_database)
        cursor.close()
        result__list = []
        for node in nodes_in_database:
            result__list.append(NodeEntity(node[1],node[2],node[3]))
        return result__list

    def update_node(self, node : NodeEntity)-> NodeEntity:
        """Updates a specific node"""
        cursor = self.connection.cursor()
        query = """
        UPDATE nodes
        SET ip = ?, port = ?
        WHERE name = ?; 
        """
        if self.check_in_database(node.name):
            logging.debug('Current node: <%s>', node)
            logging.debug('Executing UPDATE SQL query: "%s"', query)
            logging.debug('Updating values to: ip:<%s> port:<%s>', node.ip, node.port)
            cursor.execute(query, (node.ip, node.port, node.name))
            self.commit()
            logging.debug('Updated record.')
            cursor.close()
        else:
            logging.debug('Can not update non existing node with name "%s".', node.name)
            raise sqlite3.Error("Can not update non existing node")

    def delete_node_by_name(self, name : str):
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
        """Deletes the node records of the node table except the first one (device node)"""
        cursor = self.connection.cursor()
        query = 'DELETE FROM nodes WHERE id != 1;'
        logging.debug('Executing DELETE ALL SQL query: "%s"', query)
        cursor.execute(query)
        self.commit()
        logging.debug('Deleted all records from table "node"')
        cursor.close()

    def get_node_id_by_name(self, name) -> int:
        """Gets the id of the node by its name"""
        cursor = self.connection.cursor()
        query = 'SELECT id FROM nodes WHERE name = ?;'
        logging.debug('Executing SELECT SQL query: "%s" with name:<%s>', query, name)
        cursor.execute(query, (name,))
        node_id = cursor.fetchone()
        if node_id is None:
            logging.debug('No node with name "%s" exists.', name)
            return None
        logging.debug('Query executed. Result: id:<%s>', node_id[0])
        cursor.close()
        return node_id[0]

    def open_repository(self):
        """Creates the database connection"""
        self.connection = db.create_connection("pime_database.py")

    def close_repository(self):
        """Closes the database connection"""
        self.connection.close()

    def commit(self):
        """Commits the database transactions"""
        self.connection.commit()

    def check_in_database(self, name: str) -> bool:
        """Checks if a node with a specific name is in database"""
        return self.read_node_by_name(name) is not None

    def get_first(self):
        """Return the device node"""
        cursor = self.connection.cursor()
        query = "SELECT * FROM nodes WHERE id=1"
        logging.debug('Executing SELECT SQL query: "%s"', query)
        cursor.execute(query)
        first_node = cursor.fetchone()
        if first_node is None:
            logging.debug('Nodes table is empty')
            return None
        logging.debug('Query executed. Result: %s', first_node)
        result_node = NodeEntity(first_node[1],first_node[2],first_node[3])
        return result_node
 
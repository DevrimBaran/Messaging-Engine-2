import pime2.database as db
import logging
import pime2.node
import sqlite3

class NodeRepository():

    def __init__(self):
        self.connection = db.create_connection("pime_database.db")

    def create_node(self, node : pime2.node.NodeEntity):
        cursor = self.connection.cursor()
        query = 'INSERT INTO nodes(name,ip,port) VALUES(?,?,?);' 
        logging.debug('Executing SQL query: "%s"', query)
        logging.debug('Values inserted: name:<%s> ip:<%s> port:<%s>', node.name, node.ip, node.port)
        try:
            cursor.execute(query, (node.name, node.ip, node.port))
        except sqlite3.IntegrityError as integrity_err:
            logging.debug('Node with name "%s" exists already. Please only give unique names. Error: %s', node.name, integrity_err)
            raise sqlite3.IntegrityError("Duplicate Entry")
        finally:
            self.commit()
            cursor.close()

    def read_node_by_name(self, name : str) -> pime2.node.NodeEntity:
        cursor = self.connection.cursor()
        query = 'SELECT * FROM nodes WHERE name = ?;'
        logging.debug('Executing SELECT SQL query: "%s" with name:<%s>', query, name)
        cursor.execute(query, (name,))
        node_in_database = cursor.fetchone()
        if node_in_database is None:
            logging.debug('No node with name "%s" exists.', name)
            return None
        logging.debug('Query executed. Result: %s', node_in_database)
        result_node = pime2.node.NodeEntity(node_in_database[1],node_in_database[2],node_in_database[3]) 
        cursor.close()
        return result_node
     

    def update_node(self, node : pime2.node.NodeEntity)-> pime2.node.NodeEntity:
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

    def open_repository(self):
        self.connection = db.create_connection("pime_database.py")
    
    def close_repository(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def check_in_database(self, name: str) -> bool:
        return self.read_node_by_name(name) is not None
       
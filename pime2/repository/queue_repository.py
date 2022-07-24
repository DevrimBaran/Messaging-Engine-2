import logging
import sqlite3
from sqlite3 import IntegrityError


class QueueRepository:
    """database access wrapper for message_executions table"""

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def put_into_push_queue(self, message: str):
        """Saves a message from the queue in the push_queue table"""
        cursor = self.connection.cursor()
        query = 'INSERT INTO push_queue (message) VALUES(?);'
        logging.debug('Executing SQL query: "%s"', query)
        try:
            cursor.execute(query, (message,))
            self.connection.commit()
            logging.debug('Values inserted: message:<%s>', message)
        except IntegrityError:
            logging.debug("Integrity error during insert detected")
        finally:
            cursor.close()

    def delete_from_push_queue(self):
        """Deletes the first entry from the push_queue table"""
        cursor = self.connection.cursor()
        query = 'DELETE FROM push_queue WHERE (SELECT id FROM push_queue LIMIT 1);'
        logging.debug('Executing SQL query: "%s"', query)
        try:
            cursor.execute(query)
            self.connection.commit()
        except IntegrityError:
            logging.debug("Integrity error during insert detected")
        finally:
            cursor.close()

    def get_all_from_push_queue(self):
        """Returns all messages from the push_queue table"""
        cursor = self.connection.cursor()
        query = 'SELECT message FROM push_queue;'
        logging.debug('Executing SQL query: "%s"', query)
        try:
            cursor.execute(query)
            msg_in_database = cursor.fetchall()
            logging.debug('Query executed. Result: %s', msg_in_database)
            result_list = []
            if len(msg_in_database) == 0 or msg_in_database is None:
                logging.debug('No messages existing.')
                return []
            for msg in msg_in_database:
                result_list.append(msg[0])
            return result_list
        except IntegrityError:
            logging.debug("Integrity error during insert detected")
        finally:
            cursor.close()

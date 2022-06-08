import json
import logging
from sqlite3 import IntegrityError, Error
from typing import List, Optional
from pime2.entity import FlowEntity


class FlowRepository:
    """Implements node repository class"""

    def __init__(self, connection):
        self.connection = connection

    def create_flow(self, flow: FlowEntity):
        """Saves a node in database"""
        cursor = self.connection.cursor()

        # delete a flow with an existing name like this to avoid old data
        if self.check_in_database(flow.name):
            self.delete_flow_by_name(flow.name)
        #TODO: Flowoperations as json string 
        query = 'INSERT INTO flows(name, flow_ops) VALUES(?);'
        logging.debug('Executing SQL query: "%s"', query)
        logging.debug('Values inserted: name:<%s>',
                      flow.name)
        try:
            cursor.execute(query, (
               flow.name,))
            self.commit()
        except IntegrityError:
            logging.debug("Integrity error during insert detected")
        finally:
            cursor.close()

    def read_flow_by_name(self, name: str) -> Optional[FlowEntity]:
        """Return a node with a specific name from database"""
        cursor = self.connection.cursor()
        query = 'SELECT * FROM flows WHERE name = ?;'
        logging.debug('Executing SELECT SQL query: "%s" with name:<%s>', query, name)

        try:
            cursor.execute(query, (name,))
            flow_in_database = cursor.fetchone()
            if flow_in_database is None:
                logging.debug('No flow with name "%s" exists.', name)
                return None
            logging.debug('Query executed. Result: %s', flow_in_database)
            result_flow = FlowEntity(flow_in_database[1], flow_in_database[2])

            return result_flow
        finally:
            cursor.close()

    def read_all_flows(self) -> List[FlowEntity]:
        """Return every flow in the database as a list"""
        cursor = self.connection.cursor()
        query = 'SELECT * FROM flows;'
        logging.debug('Executing SELECT SQL query: "%s"', query)

        try:
            cursor.execute(query)
            flows_in_database = cursor.fetchall()
            if len(flows_in_database) == 0 or flows_in_database is None:
                logging.debug('No flows existing.')
                return []
            logging.debug('Query executed. Result: %s', flows_in_database)
            result_list = []
            #TODO: FlowOperation
            for flow in flows_in_database:
                flow_operations = [] if list(flow[2]).__len__() == 0 else flow[2].split(",")
                result_list.append(FlowEntity(flow[1], flow_operations))
            return result_list
        finally:
            cursor.close()

    def update_flow(self, flow: FlowEntity):
        """Updates a specific node"""
        cursor = self.connection.cursor()
        query = """
        UPDATE flows
        SET flow_operation = ?
        WHERE name = ?; 
        """
        try:
            if self.check_in_database(flow.name):
                logging.debug('Current flow: <%s>', flow)
                logging.debug('Executing UPDATE SQL query: "%s"', query)
                logging.debug('Updating values to: flow_operation: <%s>', flow.ops)
                #TODO: FlowOperation 
                cursor.execute(query, (
                    json.dumps(flow.ops.__dict__)))
                self.commit()
                logging.debug('Updated record.')
            else:
                logging.debug('Can not update non existing flow with name "%s".', flow.name)
                raise Error("Can not update non existing node")
        finally:
            cursor.close()

    def delete_flow_by_name(self, name: str):
        """Deletes a specific node by its name"""
        cursor = self.connection.cursor()
        if self.check_in_database(name):
            query = 'DELETE FROM flows WHERE name = ?;'
            logging.debug('Executing DELETE SQL query: "%s" with name:<%s>.', query, name)
            cursor.execute(query, (name,))
            self.commit()
            logging.debug('Deleted record with name "%s".', name)
            cursor.close()
        else:
            logging.debug('Can not delete non existing flow with name "%s".', name)
            raise Error("Can not delete non existing node")

    def delete_all(self):
        """Deletes the flow records of the flows table"""
        cursor = self.connection.cursor()
        query = 'DELETE FROM flows;'
        logging.debug('Executing DELETE ALL SQL query: "%s"', query)
        cursor.execute(query)
        self.commit()
        logging.debug('Deleted all records from table "flows"')
        cursor.close()

    def commit(self):
        """Commits the database transactions"""
        self.connection.commit()

    def check_in_database(self, name: str) -> bool:
        """Checks if a node with a specific name is in database"""
        return self.read_flow_by_name(name) is not None

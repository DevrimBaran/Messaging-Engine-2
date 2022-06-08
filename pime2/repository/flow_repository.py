import json
import logging
from sqlite3 import IntegrityError, Error
from typing import List, Optional
from pime2.entity import FlowEntity
from pime2.mapper.flow_mapper import FlowMapper


class FlowRepository:
    """Implements flow repository class"""

    def __init__(self, connection):
        self.connection = connection
        self.flow_mapper = FlowMapper()

    def create_flow(self, flow: FlowEntity):
        """Saves a flow in database"""
        cursor = self.connection.cursor()
        flow_operations = self.flow_mapper.flow_operation_to_json(flow.ops)
        # delete a flow with an existing name like this to avoid old data
        if self.check_in_database(flow.name):
            self.delete_flow_by_name(flow.name)
        query = 'INSERT INTO flows(name, ops) VALUES(?,?);'
        logging.debug('Executing SQL query: "%s"', query)
        logging.debug('Values inserted: name:<%s> ops:<%s>',
                      flow.name, flow_operations)
        try:
            cursor.execute(query, (
               flow.name, flow_operations))
            self.commit()
        finally:
            cursor.close()

    def read_flow_by_name(self, name: str) -> Optional[FlowEntity]:
        """Return a flow with a specific name from database"""
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
            result_flow = FlowEntity(flow_in_database[1], self.flow_mapper.json_to_flow_operation(flow_in_database[2]))

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
            for flow in flows_in_database:
                result_list.append(FlowEntity(flow[1], self.flow_mapper.json_to_flow_operation(flow[2])))
            return result_list
        finally:
            cursor.close()

    def update_flow(self, flow: FlowEntity):
        """Updates a specific flow"""

        cursor = self.connection.cursor()
        query = """
        UPDATE flows
        SET ops = ?
        WHERE name = ?; 
        """
        try:
            if self.check_in_database(flow.name):
                logging.debug('Current flow: <%s>', flow)
                logging.debug('Executing UPDATE SQL query: "%s"', query)
                logging.debug('Updating values to: ops: <%s>', flow.ops)
                #TODO: FlowOperation 
                flow_operations = self.flow_mapper.flow_operation_to_json(flow.ops)
                cursor.execute(query, (flow_operations, flow.name))
                self.commit()
                logging.debug('Updated record.')
            else:
                logging.debug('Can not update non existing flow with name "%s".', flow.name)
                raise Error("Can not update non existing flow")
        finally:
            cursor.close()

    def delete_flow_by_name(self, name: str):
        """Deletes a specific flow by its name"""
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
            raise Error("Can not delete non existing flow")

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
        """Checks if a flow with a specific name is in database"""
        return self.read_flow_by_name(name) is not None

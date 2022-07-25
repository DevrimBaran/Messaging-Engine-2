from datetime import datetime
import logging
import sqlite3
from typing import Optional


class ExecutionRepository:
    """database access wrapper for message_executions table"""

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def is_message_executed(self, flow_id: str, msg_id: str) -> (bool, Optional[datetime]):
        """Checks if a given message was already executed"""
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "SELECT * FROM message_executions "
                "WHERE flow_id LIKE ? "
                "AND message_id LIKE ? "
                "AND created_at > datetime('now', '-12 hours');",
                (flow_id, msg_id))
            result = cursor.fetchone()
            if result is None or len(result) == 0:
                return False, None
            return True, datetime.fromisoformat(result[3])
        finally:
            cursor.close()

    def register_execution(self, flow_id: str, msg_id: str):
        """Register execution of a single message"""
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO message_executions (flow_id, message_id, created_at) VALUES (?, ?, datetime('now'));",
                (flow_id, msg_id))
            self.connection.commit()
        finally:
            cursor.close()

    def delete_old(self):
        """Delete old data"""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM message_executions WHERE created_at < datetime('now', '-12 hours');")
        self.connection.commit()
        logging.debug('Deleted old records from table "message_executions"')
        cursor.close()

    def delete_all(self):
        """Clears message_executions table"""
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM message_executions;')
        self.connection.commit()
        logging.debug('Deleted all records from table "message_executions"')
        cursor.close()

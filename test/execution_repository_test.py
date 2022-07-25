import unittest
from datetime import datetime

from me2.repository.execution_repository import ExecutionRepository

from test.generic import GenericDatabaseTest


class ExecutionRepositoryTest(GenericDatabaseTest):
    exec_repo = None

    @classmethod
    def setUp(cls):
        super().setUp()
        cls.exec_repo = ExecutionRepository(cls.connection)
        cls.exec_repo.delete_all()

    def test_register(self):
        self.exec_repo.register_execution("test", "test")
        self.assertTrue(True)

    def test_register_and_exists(self):
        self.exec_repo.register_execution("test", "test")
        self.assertTrue(self.exec_repo.is_message_executed("test", "test"))
        self.assertTrue(isinstance(self.exec_repo.is_message_executed("test", "test")[1], datetime))
        self.assertFalse(self.exec_repo.is_message_executed("test", "test2")[0])
        self.assertFalse(self.exec_repo.is_message_executed("test2", "test")[0])

    def test_delete_old(self):
        cursor = self.connection.cursor()
        cursor.execute("""
        INSERT INTO message_executions (flow_id, message_id, created_at) VALUES
            ('old1', 'test1', datetime('now', '-1 hours')),
            ('old2', 'test2', datetime('now', '-5 hours')),
            ('old3', 'test3', datetime('now', '-11 hours')),
            ('old4', 'test4', datetime('now', '-13 hours'));
        """)
        self.connection.commit()
        cursor.execute("SELECT COUNT(*) FROM message_executions;")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(4, result[0])

        self.assertTrue(self.exec_repo.is_message_executed("old1", "test1")[0])
        self.assertTrue(self.exec_repo.is_message_executed("old2", "test2")[0])
        self.assertTrue(self.exec_repo.is_message_executed("old3", "test3")[0])
        self.assertFalse(self.exec_repo.is_message_executed("old4", "test4")[0])
        self.exec_repo.delete_old()
        self.assertFalse(self.exec_repo.is_message_executed("old4", "test4")[0])
        cursor.execute("SELECT COUNT(*) FROM message_executions;")
        result = cursor.fetchone()
        cursor.close()
        self.assertIsNotNone(result)
        self.assertEqual(3, result[0])


if __name__ == '__main__':
    unittest.main()

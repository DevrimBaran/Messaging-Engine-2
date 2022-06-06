import imp
import unittest
import os
import pime2.database as db
from pime2.repository.node_repository import NodeRepository

from pime2 import database
from pime2.config import load_app_config
from pime2.repository.node_repository import NodeRepository
from pime2.service.node_service import NodeService


class DatabaseTest(unittest.TestCase):
    node_repo: NodeRepository = None

    @classmethod
    def setUp(cls):
        if os.path.exists("testDatabase.db"):
            db.disconnect(cls.connection)
            os.remove("testDatabase.db")
        cls.connection = db.create_connection("testDatabase.db")
        cls.node_repo = NodeRepository(cls.connection)
        database.create_default_tables(cls.connection, NodeService())

    def test_create_default_tables(self):
        db.create_default_tables(self.connection)
        self.node_repo.delete_all()

        sql_insert_testdata = """INSERT INTO nodes (id, name, ip, port, sensor_skills, actuator_skills)
                                    VALUES 
                                        (1, 'node1', "10.10.10.1", 5683,"TEMP","LIGHT"),
                                        (2, 'node2', "10.10.10.2", 5683,"TEMP","LIGHT"),
                                        (3, 'node3', "10.10.10.3", 5683,"TEMP","LIGHT");"""

        sql_select_testdata = """SELECT * FROM nodes"""

        cursor = self.connection.cursor()
        cursor.execute(sql_insert_testdata)
        cursor.execute(sql_select_testdata)
        self.connection.commit()

        result = cursor.fetchall()
        cursor.close()

        self.assertEqual(
            [(1, 'node1', '10.10.10.1', 5683, "TEMP", "LIGHT"), (2, 'node2', "10.10.10.2", 5683, "TEMP", "LIGHT"),
             (3, 'node3', "10.10.10.3", 5683, "TEMP", "LIGHT")],
            result)

    @classmethod
    def tearDownClass(cls):
        database.disconnect(cls.connection)
        os.remove("testDatabase.db")


if __name__ == '__main__':
    unittest.main()

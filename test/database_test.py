import unittest
import os

from pime2 import database
from pime2.config import load_app_config, get_me_conf
from pime2.repository.node_repository import NodeRepository


class DatabaseTest(unittest.TestCase):
    node_repo: NodeRepository = None
    connection = None

    @classmethod
    def setUp(cls):
        if os.path.exists("testDatabase.db"):
            database.disconnect(cls.connection)
            os.remove("testDatabase.db")
        load_app_config("me.yaml")
        cls.connection = database.create_connection("testDatabase.db")
        cls.node_repo = NodeRepository(cls.connection)
        database.create_default_tables(cls.connection)

    def test_create_default_tables(self):
        self.node_repo.delete_all()

        database.create_default_tables(self.connection)

        sql_insert_testdata = """INSERT INTO nodes (name, ip, port)
                                    VALUES 
                                        ('node1', "10.10.10.1", 5683),
                                        ('node2', "10.10.10.2", 5683),
                                        ('node3', "10.10.10.3", 5683);"""

        sql_select_testdata = """SELECT name, ip, port FROM nodes;"""

        cursor = self.connection.cursor()
        cursor.execute(sql_insert_testdata)
        cursor.execute(sql_select_testdata)
        self.connection.commit()

        result = cursor.fetchall()
        cursor.close()

        conf = get_me_conf()

        self.assertEqual(
            [(conf.instance_id, conf.host, conf.port),
             ('node1', '10.10.10.1', 5683), ('node2', "10.10.10.2", 5683), ('node3', "10.10.10.3", 5683)],
            result)

    @classmethod
    def tearDownClass(cls):
        database.disconnect(cls.connection)
        os.remove("testDatabase.db")


if __name__ == '__main__':
    unittest.main()

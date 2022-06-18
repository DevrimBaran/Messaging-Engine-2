import unittest
import os

from pime2 import database
from pime2.config import get_me_conf, load_app_config
from pime2.repository.node_repository import NodeRepository
from pime2.service.node_service import NodeService
from test.generic import GenericDatabaseTest


class DatabaseTest(GenericDatabaseTest):
    node_repo: NodeRepository = None

    @classmethod
    def setUp(cls):
        super().setUp()
        cls.node_repo = NodeRepository(cls.connection)
        cls.node_repo.delete_all()

    def test_create_default_tables(self):
        self.node_repo.delete_all()
        database.create_default_tables(self.connection, NodeService())

        sql_insert_testdata = """INSERT INTO nodes (name, ip, port)
                                    VALUES 
                                        ('node1', "10.10.10.1", 5683),
                                        ('node2', "10.10.10.2", 5683),
                                        ('node3', "10.10.10.3", 5683);"""

        sql_select_testdata = """SELECT name, ip, port FROM nodes ORDER BY id;"""

        cursor = self.connection.cursor()
        cursor.execute(sql_insert_testdata)
        cursor.execute(sql_select_testdata)
        self.connection.commit()

        result = cursor.fetchall()
        cursor.close()

        conf = get_me_conf()

        self.assertEqual(
            [(conf.instance_id, conf.host, conf.port),
             ('node1', '10.10.10.1', 5683),
             ('node2', "10.10.10.2", 5683),
             ('node3', "10.10.10.3", 5683)],
            result)


if __name__ == '__main__':
    unittest.main()

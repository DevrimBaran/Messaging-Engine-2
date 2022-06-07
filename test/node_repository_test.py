import unittest
import os
import pime2.database as db
from pime2.config import load_app_config
from pime2.repository.node_repository import NodeRepository as repo
from pime2.entity import NodeEntity as Node
from sqlite3 import Error

from pime2.service.node_service import NodeService


class NodeRepositoryTest(unittest.TestCase):
    connection = None
    node_repo = None

    @classmethod
    def setUp(cls):
        if os.path.exists("testDatabase.db"):
            db.disconnect(cls.connection)
            os.remove("testDatabase.db")
        cls.connection = db.create_connection("testDatabase.db")
        load_app_config("me.yaml")
        cls.node_repo = repo(cls.connection)
        db.create_default_tables(cls.connection, NodeService())
        cls.node_repo.delete_all()

    def get_node_list(self):
        return [Node("node1", "10.10.10.1", 5683, ["TEMPERATURE"], ["LIGHT"]),
                Node("node2", "10.10.10.1", 5683, ["TEMPERATURE"], ["LIGHT"]),
                Node("node3", "10.10.10.1", 5683, ["TEMPERATURE"], [
                    "LIGHT"]), Node("node4", "10.10.10.1", 5683, ["TEMPERATURE"], ["LIGHT"]),
                Node("node5", "10.10.10.1", 5683, ["TEMPERATURE"], ["LIGHT"]),
                Node("node6", "10.10.10.1", 5683, ["TEMPERATURE"], ["LIGHT"])]

    def test_read_node_by_name(self):
        simple_node = Node("simple_node", "10.10.10.1",
                           5683, ["TEMPERATURE"], ["LIGHT"])
        self.node_repo.create_node(simple_node)
        result_node = self.node_repo.read_node_by_name("simple_node")
        self.assertEqual(simple_node, result_node)
        result_node_none = self.node_repo.read_node_by_name("Test")
        self.assertIsNone(result_node_none)

    def test_read_all_nodes(self):
        node_list = self.get_node_list()
        for node in node_list:
            self.node_repo.create_node(node)
        result = self.node_repo.read_all_nodes()
        self.assertEqual(node_list, result)

    def test_read_all_nodes_empty(self):
        self.assertEqual([], self.node_repo.read_all_nodes())

    def test_create_simple_node(self):
        simple_node = Node("simple_node", "10.10.10.1",
                           5683, ["TEMPERATURE"], ["LIGHT"])
        self.node_repo.create_node(simple_node)
        result = self.node_repo.read_all_nodes()
        self.assertEqual(simple_node, result[0])

    def test_create_node_with_sensor(self):
        node_only_sensor_multiple = Node("node_sens", "10.10.10.1", 5683, ["TEMPERATURE", "LIGHT", "HUMIDITY"], [])
        self.node_repo.create_node(node_only_sensor_multiple)
        result = self.node_repo.read_all_nodes()
        self.assertEqual(node_only_sensor_multiple, result[0])

    def test_create_node_with_actuator(self):
        node_only_actuator = Node("node_act", "10.10.10.1", 5683, [], ["LIGHT", "MOTOR", "SPEAKER"])
        self.node_repo.create_node(node_only_actuator)
        result = self.node_repo.read_all_nodes()
        self.assertEqual(node_only_actuator, result[0])

    def test_create_node_with_sensor_and_actuator(self):
        node_sensor_and_actuator = Node("node_sens_act", "10.10.10.1", 5683, ["TEMPERATURE", "LIGHT", "HUMIDITY"],
                                        ["LIGHT", "MOTOR", "SPEAKER"])
        self.node_repo.create_node(node_sensor_and_actuator)
        result = self.node_repo.read_all_nodes()
        self.assertEqual(node_sensor_and_actuator, result[0])

    def test_create_node_no_sensor_and_no_actuator(self):

        node_no_sensor_and_no_actuator = Node(
            "node_no_sens_no_act", "10.10.10.1", 5683, [], [])
        self.node_repo.create_node(node_no_sensor_and_no_actuator)
        result = self.node_repo.read_all_nodes()
        self.assertEqual(node_no_sensor_and_no_actuator, result[0])

    def test_delete_all(self):
        node_list = self.get_node_list()
        for node in node_list:
            self.node_repo.create_node(node)
        result = self.node_repo.read_all_nodes()
        self.assertEqual(node_list, result)
        self.node_repo.delete_all()
        result = self.node_repo.read_all_nodes()
        self.assertEqual(0, result.__len__())

    def test_delete_node_by_name(self):
        node_list = self.get_node_list()
        for node in node_list:
            self.node_repo.create_node(node)
        result = self.node_repo.read_all_nodes()
        self.assertEqual(node_list, result)
        self.node_repo.delete_node_by_name("node1")
        self.assertIsNone(self.node_repo.read_node_by_name("node1"))
        with self.assertRaises(Error):
            self.node_repo.delete_node_by_name("Test")

    def test_get_node_id_by_name(self):
        node_list = self.get_node_list()
        for node in node_list:
            self.node_repo.create_node(node)
        result_id = self.node_repo.get_node_id_by_name("node1")
        self.assertEqual(1, result_id)
        self.assertIsNone(self.node_repo.get_node_id_by_name("Test"))

    def test_check_in_database(self):
        node_list = self.get_node_list()
        for node in node_list:
            self.node_repo.create_node(node)
        self.assertEqual(True, self.node_repo.check_in_database("node1"))
        self.assertEqual(False, self.node_repo.check_in_database("Test"))

    def test_update_node(self):
        node_list = self.get_node_list()
        for node in node_list:
            self.node_repo.create_node(node)
        self.assertEqual(node_list, self.node_repo.read_all_nodes())
        node_list_update = [Node("node1", "10.10.10.1", 5683, ["TEMPERATURE"], ["LIGHT", "SPEAKER"]),
                            Node("node2", "10.10.10.1", 5683, ["TEMPERATURE"], ["LIGHT"]),
                            Node("node3", "10.10.10.1", 5683, ["TEMPERATURE"], ["LIGHT"]),
                            Node("node4", "10.10.10.1", 5683, ["TEMPERATURE"], ["LIGHT"]),
                            Node("node5", "10.10.10.1", 5683, ["TEMPERATURE"], ["LIGHT"]),
                            Node("node6", "10.10.10.1", 5683, ["TEMPERATURE", "HUMIDITY"], ["LIGHT"])
                            ]
        for node_update in node_list_update:
            self.node_repo.update_node(node_update)
        self.assertEqual(node_list_update, self.node_repo.read_all_nodes())
        with self.assertRaises(Error):
            self.node_repo.update_node(Node("Test", "127.1.1.1", 5863, set("TEMP"), set("SPEAKER")))

    @classmethod
    def tearDownClass(cls):
        db.disconnect(cls.connection)
        os.remove("testDatabase.db")


if __name__ == '__main__':
    unittest.main()

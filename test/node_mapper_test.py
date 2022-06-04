import json
import unittest
import os
import pime2.database as db
from pime2.mapper.node_mapper import NodeMapper
from pime2.repository.node_repository import NodeRepository
from pime2.entity import NodeEntity as Node


class NodeMapperTest(unittest.TestCase):
    connection = None
    node_repo = None

    @classmethod
    def setUpClass(cls):
        cls.connection = db.create_connection("testDatabase.db")
        cls.node_repo = NodeRepository(cls.connection)
        cls.node_mapper = NodeMapper()
        db.create_default_tables(cls.connection)

    @classmethod
    def setUp(cls):
        if os.path.exists("testDatabase.db"):
            db.disconnect(cls.connection)
            os.remove("testDatabase.db")
        cls.connection = db.create_connection("testDatabase.db")
        cls.node_repo = NodeRepository(cls.connection)
        db.create_default_tables(cls.connection)
        cls.node_repo.delete_all()

    def get_node_list(self):
        return [
            Node("node1", "10.10.10.1", 5683, ["TEMPERATURE"], ["LIGHT"]), 
            Node("node2", "10.10.10.1", 5683, [], ["LIGHT"]), 
            Node("node3", "10.10.10.1", 5683, ["TEMPERATURE"], []), 
            Node("node4", "10.10.10.1", 5683, ["TEMPERATURE","LIGHT"], ["LIGHT"]), 
            Node("node5", "10.10.10.1", 5683, ["TEMPERATURE"], ["LIGHT","SPEAKER"]), 
            Node("node6", "10.10.10.1", 5683, ["TEMPERATURE","SOUND"], ["LIGHT","SPEAKER"]),
            Node("node7", "10.10.10.1", 5683, [], [])]
    def get_node_list_json(self):
        return [
            '{"name": "node1", "ip": "10.10.10.1", "port": 5683, "sensor_skills": ["TEMPERATURE"], "actuator_skills": ["LIGHT"]}',
            '{"name": "node2", "ip": "10.10.10.1", "port": 5683, "sensor_skills": [], "actuator_skills": ["LIGHT"]}',
            '{"name": "node3", "ip": "10.10.10.1", "port": 5683, "sensor_skills": ["TEMPERATURE"], "actuator_skills": []}',
            '{"name": "node4", "ip": "10.10.10.1", "port": 5683, "sensor_skills": ["TEMPERATURE","LIGHT"], "actuator_skills": ["LIGHT"]}',
            '{"name": "node5", "ip": "10.10.10.1", "port": 5683, "sensor_skills": ["TEMPERATURE"], "actuator_skills": ["LIGHT","SPEAKER"]}',
            '{"name": "node6", "ip": "10.10.10.1", "port": 5683, "sensor_skills": ["TEMPERATURE","SOUND"], "actuator_skills": ["LIGHT","SPEAKER"]}',
            '{"name": "node7", "ip": "10.10.10.1", "port": 5683, "sensor_skills": [], "actuator_skills": []}'
        ]

    def get_json(self):
        return [
            '[',
            '{"name": "node1", "ip": "10.10.10.1", "port": 5683, "sensor_skills": ["TEMPERATURE"], "actuator_skills": ["LIGHT"]},',
            '{"name": "node2", "ip": "10.10.10.1", "port": 5683, "sensor_skills": [], "actuator_skills": ["LIGHT"]},',
            '{"name": "node3", "ip": "10.10.10.1", "port": 5683, "sensor_skills": ["TEMPERATURE"], "actuator_skills": []},',
            '{"name": "node4", "ip": "10.10.10.1", "port": 5683, "sensor_skills": ["TEMPERATURE","LIGHT"], "actuator_skills": ["LIGHT"]},',
            '{"name": "node5", "ip": "10.10.10.1", "port": 5683, "sensor_skills": ["TEMPERATURE"], "actuator_skills": ["LIGHT","SPEAKER"]},',
            '{"name": "node6", "ip": "10.10.10.1", "port": 5683, "sensor_skills": ["TEMPERATURE","SOUND"], "actuator_skills": ["LIGHT","SPEAKER"]},',
            '{"name": "node7", "ip": "10.10.10.1", "port": 5683, "sensor_skills": [], "actuator_skills": []}',
            ']'
        ]

    def test_json_to_entity(self):
        node_list = self.get_node_list()
        for node in node_list:
            self.node_repo.create_node(node)
        node_list_json = self.get_node_list_json()
        node_list_read = self.node_repo.read_all_nodes()
        for ind in range(node_list_json.__len__()):
            self.assertEqual(node_list_read[ind],self.node_mapper.json_to_entity(node_list_json[ind]))


    def test_entity_list_to_json(self):
        node_list = self.get_node_list()
        node_list_json = self.get_json()      
        self.assertEqual(json.loads(("").join(node_list_json)),json.loads(self.node_mapper.entity_list_to_json(node_list)))

    @classmethod
    def tearDownClass(cls):
        db.disconnect(cls.connection)
        os.remove("testDatabase.db")


if __name__ == '__main__':
    unittest.main()

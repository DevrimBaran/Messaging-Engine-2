import json
import unittest

from me2.entity import NodeEntity
from me2.mapper.node_mapper import NodeMapper


class NodeMapperTest(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.node_mapper = NodeMapper()

    def get_node_list(self):
        return [
            NodeEntity("node1", "10.10.10.1", 5683, ["TEMPERATURE"], ["LIGHT"]),
            NodeEntity("node2", "10.10.10.1", 5683, [], ["LIGHT"]),
            NodeEntity("node3", "10.10.10.1", 5683, ["TEMPERATURE"], []),
            NodeEntity("node4", "10.10.10.1", 5683, ["TEMPERATURE", "LIGHT"], ["LIGHT"]),
            NodeEntity("node5", "10.10.10.1", 5683, ["TEMPERATURE"], ["LIGHT", "SPEAKER"]),
            NodeEntity("node6", "10.10.10.1", 5683, ["TEMPERATURE", "SOUND"], ["LIGHT", "SPEAKER"]),
            NodeEntity("node7", "10.10.10.1", 5683, [], [])]

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

    def test_node_list_conversion(self):
        node_list_read = self.get_node_list()
        node_list_json = self.get_node_list_json()
        for ind in range(len(node_list_json)):
            self.assertEqual(node_list_read[ind], self.node_mapper.json_to_entity(node_list_json[ind]))

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
        node_list_json = self.get_node_list_json()
        node_list_read = self.get_node_list()
        for ind in range(len(node_list_json)):
            self.assertEqual(node_list_read[ind], self.node_mapper.json_to_entity(node_list_json[ind]))

    def test_entity_list_to_json(self):
        node_list = self.get_node_list()
        node_list_json = self.get_json()
        self.assertEqual(json.loads("".join(node_list_json)),
                         json.loads(self.node_mapper.entity_list_to_json(node_list)))


if __name__ == '__main__':
    unittest.main()

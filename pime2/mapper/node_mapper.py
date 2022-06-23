import json
import logging
from typing import List
from pime2.entity import NodeEntity



class NodeMapper:
    """Implements node mapper class"""

    def json_to_entity(self, json_str: str) -> NodeEntity:
        """Converts json to entity"""
        json_obj = json.loads(json_str)
        name = json_obj['name']
        ip_addr = json_obj['ip']
        port = json_obj['port']
        sensor_skills = [] if "sensor_skills" not in json_obj else json_obj["sensor_skills"]
        actuator_skills = [] if "actuator_skills" not in json_obj else json_obj["actuator_skills"]
        node = NodeEntity(name, ip_addr, port, sensor_skills, actuator_skills)
        logging.info("JSON to entity : <%s>", node)
        return node

    def entity_list_to_json(self, node_list: List[NodeEntity]) -> str:
        """Converts a list of entities to json"""
        node_json_string = json.dumps(node_list, default=lambda o: getattr(o, '__dict__', str(o)))
        logging.info("Entity list to json : <%s>", node_json_string)
        return node_json_string

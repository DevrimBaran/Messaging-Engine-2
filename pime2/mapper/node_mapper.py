import json
import logging
from typing import List

from pime2.entity import NodeEntity


class NodeMapper:
    """Implements node mapper class"""

    def json_to_entity(self, json_str: str) -> NodeEntity:
        """Converts json to entity"""
        json_obj = json.loads(json_str)
        
        node = NodeEntity(json_obj['name'], json_obj['ip'], json_obj['port'],json_obj['sensor_skills'], json_obj['actuator_skills'])
        logging.info("JSON to entity : <%s>", node)
        return node

    def entity_list_to_json(self, node_list: List[NodeEntity]) -> str:
        """Converts a list of entities to json"""
        node_array = []
        for node in node_list:
            node_array.append(node.__dict__)
        node_json_string = json.dumps(node_array)
        logging.info("Entity list to json : <%s>", node_json_string)
        return node_json_string

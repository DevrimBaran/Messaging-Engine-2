import json
import logging
from pime2.entity.node import NodeEntity


class NodeMapper():
    """Implements node mapper class"""
    def entity_to_json(self, node:NodeEntity) -> str:
        """Converts entity to json"""
        node_dict = {}
        node_dict['name'] = node.name
        node_dict['ip'] = node.ip
        node_dict['port'] = node.port
        node_json_string = json.dumps(node_dict)
        logging.info("Entity to JSON : <%s>",node_json_string)
        return node_json_string

    def json_to_entity(self, json_str:str) -> NodeEntity:
        """Converts json to entity"""
        json_obj = json.load(json_str)
        node = NodeEntity(json_obj['name'],json_obj['ip'],json_obj['port'])
        logging.info("JSON to entity : <%s>",node)
        return node

    def entity_list_to_json(self, node_list:list[NodeEntity]) -> str:
        """Converts a list of entities to json"""
        node_array = []
        for node in node_list:
            node_dict = {}
            node_dict['name']= node.name
            node_dict['ip'] = node.ip
            node_dict['port'] = node.port
            node_array.append(node_dict)
        node_json_string = json.dumps(node_array)
        logging.info("Entity list to json : <%s>",node_json_string)
        return node_json_string

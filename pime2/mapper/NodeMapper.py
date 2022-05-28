from msilib.schema import Error
from pime2.entity.node import NodeEntity
import json
import logging

class NodeMapper():
    def entity_to_json(node:NodeEntity) -> str:
        node_dict = {}
        node_dict['name'] = node.name
        node_dict['ip'] = node.ip
        node_dict['port'] = node.port
        node_json_string = json.dump(node_dict)
        return node_json_string

    def json_to_entity(json_str:str) -> NodeEntity:
        json_obj = json.load(json_str)
        required_fields = [
            "name",
            "ip",
            "port",
        ]
        for i in required_fields:
                if i not in json_obj or json_obj[i] is None:
                    logging.error("Required fields are missing!")
                    raise Error("Required fields are missing!")
        node = NodeEntity(json_obj['name'],json_obj['ip'],json_obj['port'])
        return node

    def entity_list_to_json(node_list:list[NodeEntity]) -> str:
        node_array = []
        for node in node_list:
            node_dict = {}
            node_dict['name']= node.name
            node_dict['ip'] = node.ip
            node_dict['port'] = node.port
            node_array.append(node_dict)
        node_json_string = json.dumps(node_array)
        return node_json_string


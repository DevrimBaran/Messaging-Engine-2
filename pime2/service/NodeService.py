import logging
from sqlite3 import IntegrityError
from pime2.entity.node import NodeEntity
from pime2.message import NodeCreateResultMessage
from pime2.repository.NodeRepository import NodeRepository
from pime2.mapper.NodeMapper import NodeMapper
import json
from json import JSONDecodeError
from aiocoap import Message, Code
from pime2.push_queue import get_push_queue
import re as regex

class NodeService():

    def __init__(self):
        """Initialize NodeRepository and NodeMapper"""
        self.node_repository = NodeRepository()
        self.node_mapper = NodeMapper()

    def entity_to_json(self, node: NodeEntity) -> str:
        """Convert node entity to a json"""
        return self.node_mapper.entity_to_json(node)

    def json_to_entity(self, node_json: str) -> NodeEntity:
        """Convert json to a node entity"""
        return self.node_mapper.json_to_entity(node_json)
    
    def put_node(self, node: NodeEntity):
        """Save a node in the database"""
        self.node_repository.create_node(node)

    def get_all_nodes_as_json(self) -> str:
        """Get all nodes as a json string"""
        node_list = self.node_repo.read_all_nodes()
        node_json_string = self.node_mapper.entity_list_to_json(node_list)
        return node_json_string
    
    async def handle_incoming_node(self, request) -> Message:
        """Handles incoming node request and saves it to the database if everything is valid"""
        try:
            self.validate_json_node(request)
            node_record = self.json_to_entity(request)
            self.put_node(node_record)
            await get_push_queue().put(json.dumps(NodeCreateResultMessage(node_record).__dict__))
            return Message(payload=b"OK", code=Code.CREATED)
        except JSONDecodeError as ex:
            logging.warning("Problem processing request: %s", ex)
        except ValueError as val_ex:
            logging.warning(
                "Bad input. Please correct node ip, node port and node name! Error: %s", val_ex)
        except IntegrityError as integ_ex:
            logging.warning("Duplicate Entry. Can not process.")
        return Message(payload=b"INVALID REQUEST", code=Code.BAD_REQUEST)

    def validate_json_node(self, json_node):
        """Validates json node, raises error if json is invalid"""
        required_fields = [
        "name",
        "ip",
        "port",
        ]
        ipv4_regex = "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        name_regex = "^[a-zA-Z0-9_.-]{3,128}$"
        # parse node record from request payload - if possible
        if len(json_node.payload) > 2048:
            return Message(payload=b"INVALID REQUEST", code=Code.BAD_REQUEST)
        node = json.loads(json_node.payload)

        for i in required_fields:
            if i not in node or node[i] is None:
                return Message(payload=b"INVALID REQUEST, MISSING PROPERTY", code=Code.BAD_REQUEST)
            if (regex.match(ipv4_regex, node["ip"]) is not None) and (regex.match(name_regex, node["name"]) is not None) and (node["port"] > 0 and node["port"] <= 65535):
                pass
            else:
                raise ValueError("Bad Input. Invalid json!")
    
    def get_own_node(self) -> NodeEntity:
        """Gets the first node in the database which is the device itself"""
        return self.node_repository.get_first()
    
    
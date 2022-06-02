import re as regex
import logging
import json
from json import JSONDecodeError
from sqlite3 import IntegrityError
from typing import List
from aiocoap import Message, Code

from pime2.config import get_me_conf
from pime2.database import get_db_connection
from pime2.entity import NodeEntity
from pime2.message import NodeCreateResultMessage
from pime2.repository.node_repository import NodeRepository
from pime2.mapper.node_mapper import NodeMapper
from pime2.push_queue import get_push_queue


class NodeService:
    """Implements node service class"""

    def __init__(self):
        """Initialize NodeRepository and NodeMapper"""
        self.node_repository = NodeRepository(get_db_connection())
        self.node_mapper = NodeMapper()

    def entity_to_json(self, node: NodeEntity) -> str:
        """Convert node entity to a json"""
        return json.dumps(node.__dict__)

    def json_to_entity(self, node_json: str) -> NodeEntity:
        """Convert json to a node entity"""
        return self.node_mapper.json_to_entity(node_json)

    def is_node_remote(self, node: NodeEntity) -> bool:
        """
        Method to check if a node is remote
        :param node:
        :return:
        """
        return node.name != get_me_conf().instance_id

    def put_node(self, node):
        """Save a node in the database"""
        if isinstance(node, NodeEntity):
            self.node_repository.create_node(node)
        elif isinstance(node, str):
            node = self.json_to_entity(node)
            self.node_repository.create_node(node)
        else:
            # TODO: Vielleicht nen anderen Error benutzen?
            raise ValueError("Bad Input")

    def get_all_nodes(self) -> List[NodeEntity]:
        """
        Method to return all nodes of this me2 instance
        :return:
        """
        node_list = self.node_repository.read_all_nodes()
        if node_list is None:
            return []
        return node_list
    def remove_node(self, node) -> bool:
        """Removes a node from the database"""
        if isinstance(node, NodeEntity):
            self.node_repository.delete_node_by_name(node.name)
            return True
        if isinstance(node, str):
            node = self.json_to_entity(node)
            self.node_repository.delete_node_by_name(node.name)
            return True
        return False

    def get_all_nodes_as_json(self) -> str:
        """Get all nodes as a json string"""
        node_list = self.node_repository.read_all_nodes()
        node_json_string = self.node_mapper.entity_list_to_json(node_list)
        return node_json_string

    def get_neighbors_as_entity(self) -> list:
        """Get all nodes as a json string"""
        node_list = self.node_repository.read_all_neighbors()
        return node_list

    def get_all_neighbor_nodes(self) -> List[NodeEntity]:
        """Get all nodes except the own node"""
        node_list = self.get_neighbors_as_entity()
        return node_list

    async def handle_incoming_node(self, request) -> Message:
        """Handles incoming node request and saves it to the database if everything is valid"""
        try:
            self.validate_request(request)
            node_json = request.payload.decode()
            node_record = self.json_to_entity(node_json)
            await get_push_queue().put(json.dumps(NodeCreateResultMessage(node_record).__dict__))
            return Message(payload=b"OK", code=Code.CREATED)
        except JSONDecodeError as ex:
            logging.warning("Problem processing request: %s", ex)
        except ValueError as val_ex:
            logging.warning(
                "Bad input. Please correct node ip, node port and node name! Error: %s", val_ex)
        except IntegrityError as integ_ex:
            logging.warning("Duplicate Entry. Can not process. Error: <%s>", integ_ex)
        return Message(payload=b"INVALID REQUEST", code=Code.BAD_REQUEST)

    def validate_request(self, request):
        """Validates request, return invalid request if request is invalid"""
        if len(request.payload) > 2048:
            raise JSONDecodeError(msg="Input too big", doc="request", pos=2048)
        return self.validate_request_payload(request)

    def validate_request_payload(self, request):
        """Validate the payload of the request whether it fits the specifications"""
        required_fields = [
            "name",
            "ip",
            "port",
        ]
        ipv4_regex = "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        name_regex = "^[a-zA-Z0-9_.-]{3,128}$"
        node = json.loads(request.payload)
        for i in required_fields:
            if i not in node or node[i] is None:
                return Message(payload=b"INVALID REQUEST, MISSING PROPERTY", code=Code.BAD_REQUEST)
            ipv4_regex_res = regex.match(ipv4_regex, node["ip"])
            name_regex_res = regex.match(name_regex, node["name"])
            node_match_res = node["port"] > 0 and node["port"] <= 65535
            if ipv4_regex_res and name_regex_res and node_match_res:
                pass
            else:
                raise ValueError("Bad Input. Invalid json!")
            return True

    def get_own_node(self) -> Optional[NodeEntity]:
        """Gets the first node in the database which is the device itself"""
        return self.node_repository.read_node_by_name(get_me_conf().instance_id)

    def delete_all_nodes(self):
        """Deletes all nodes from the database"""
        self.node_repository.delete_all()

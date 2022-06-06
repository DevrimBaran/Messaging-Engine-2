import json

from json import JSONDecodeError
from typing import List, Optional
from aiocoap import Message, Code

from pime2.database import get_db_connection
from pime2.entity import NodeEntity

from pime2.config import get_me_conf
from pime2.database import get_db_connection
from pime2.entity import NodeEntity
from pime2.repository.node_repository import NodeRepository
from pime2.mapper.node_mapper import NodeMapper
from pime2.push_queue import get_push_queue
from pime2.config import get_me_conf


class NodeService:
    """Implements node service class"""

    def __init__(self):
        """Initialize NodeRepository and NodeMapper"""
        self.node_repository = NodeRepository(get_db_connection())
        self.node_mapper = NodeMapper()

    def entity_to_json(self, node: NodeEntity) -> str:
        """Convert node entity to a json"""
        return json.dumps(node.__dict__, default=str)

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
            raise TypeError("Bad Input")

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

    def get_all_nodes(self) -> List[NodeEntity]:
        """
        Method to return all nodes of this me2 instance
        :return:
        """
        node_list = self.node_repository.read_all_nodes()
        if node_list is None:
            return []
        return node_list

    def get_all_nodes_as_json(self) -> str:
        """Get all nodes as a json string"""
        node_list = self.node_repository.read_all_nodes()
        node_json_string = self.node_mapper.entity_list_to_json(node_list)
        return node_json_string

    def get_own_node(self) -> Optional[NodeEntity]:
        """Gets the first node in the database which is the device itself"""
        return self.node_repository.read_node_by_name(get_me_conf().instance_id)

    def delete_all_nodes(self):
        """Deletes all nodes from the database"""
        self.node_repository.delete_all()

    def get_neighbors_as_entity(self) -> list:
        """Get all nodes as a json string"""
        node_list = self.node_repository.read_all_nodes()
        return node_list

    def get_all_neighbor_nodes(self) -> List[NodeEntity]:
        """Get all nodes except the own node"""
        return self.node_repository.read_all_nodes()

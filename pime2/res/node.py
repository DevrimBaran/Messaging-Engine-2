import json
import logging
from json import JSONDecodeError

import regex
from aiocoap import resource, Message, Code

from pime2.mapper.node_mapper import NodeMapper
from pime2.message import NodeCreateResultMessage
from pime2.push_queue import get_push_queue
from pime2.service.node_service import NodeService


class Node(resource.Resource):
    """
    Node Resource
    """

    def __init__(self):
        self.node_service = NodeService()

    async def render_put(self, request):
        """
        this method assumes json formatted input of a node record

        :param request:
        :return:
        """
        response = await self.handle_incoming_node(request)
        logging.info("Node create response: %s", response)
        return response

    async def render_get(self, request):
        """
        handle GET request to /nodes
        Return a json which includes every node in the database

        :param request:
        :return:
        """
        node_json_string = self.node_service.get_all_nodes_as_json()
        logging.info("Response JSON: %s", node_json_string)
        return Message(payload=node_json_string.encode())

    async def render_delete(self, request):
        """
        handle DELETE request to /nodes
        Deletes all nodes from the database

        :param request:
        :return:
        """
        self.node_service.delete_all_nodes()
        return Message(payload=b'Deleted all nodes')

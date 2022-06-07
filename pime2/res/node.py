import ipaddress
import json
import logging
from json import JSONDecodeError

import re
from aiocoap import resource, Message, Code

from pime2 import NAME_REGEX, CHAINED_NAME_REGEX
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

    async def handle_incoming_node(self, request) -> Message:
        """Handles incoming node request and saves it to the database if everything is valid"""
        try:
            is_valid = await self.is_request_valid(request)
            if not is_valid:
                return Message(payload=b"INVALID REQUEST, MISSING OR INVALID PROPERTY", code=Code.BAD_REQUEST)

            node_json = request.payload.decode()
            node_entity = NodeMapper().json_to_entity(node_json)
            await get_push_queue().put(json.dumps(NodeCreateResultMessage(node_entity).__dict__))
            return Message(payload=b"OK", code=Code.CREATED)
        except JSONDecodeError as ex:
            logging.warning("Problem encoding request: %s", ex)
        return Message(payload=b"INVALID REQUEST", code=Code.BAD_REQUEST)

    async def is_request_valid(self, request) -> bool:
        """Validate the payload of the request whether it fits the specifications"""
        if len(request.payload) > 2048:
            raise JSONDecodeError(msg="Input too big", doc="request", pos=2048)

        required_fields = [
            "name",
            "ip",
            "port",
        ]

        node = json.loads(request.payload)
        for i in required_fields:
            if i not in node or node[i] is None:
                return False
        name_regex_res = re.match(NAME_REGEX, node["name"])
        node_match_res = 0 < node["port"] <= 65535

        are_fields_valid = name_regex_res and node_match_res
        if not are_fields_valid:
            return False

        is_ip_valid = False
        try:
            ipaddress.ip_address(node["ip"])
            is_ip_valid = True
        except ValueError:
            is_ip_valid = False

        if not is_ip_valid:
            return False

        for i in ["sensor_skills", "actuator_skills"]:
            if i in node and len(node[i]) > 0 and not re.match(CHAINED_NAME_REGEX, node[i]):
                return False
        return True

import json
import re
import logging
from json import JSONDecodeError
import sqlite3
from sys import exc_info

import aiocoap
from aiocoap import resource

from pime2.message import NodeCreateResultMessage
from pime2.node import NodeEntity
from pime2.push_queue import get_push_queue
from pime2.repository.NodeRepository import NodeRepository


class Node(resource.Resource):
    """
    Node Resource
    """

    async def render_put(self, request):
        """
        this method assumes json formatted input of a node record

        :param request:
        :return:
        """
        node_repository = NodeRepository()
        required_fields = [
            "name",
            "ip",
            "port",
        ]
        ipv4_regex = "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        name_regex = "^[a-zA-Z0-9_.-]{3,128}$"
        # parse node record from request payload - if possible
        try:
            if len(request.payload) > 2048:
                return aiocoap.Message(payload=b"INVALID REQUEST", code=aiocoap.Code.BAD_REQUEST)
            node = json.loads(request.payload)

            for i in required_fields:
                if i not in node or node[i] is None:
                    return aiocoap.Message(payload=b"INVALID REQUEST, MISSING PROPERTY", code=aiocoap.Code.BAD_REQUEST)
                if (re.match(ipv4_regex, node["ip"]) is not None) and (re.match(name_regex, node["name"]) is not None) and (node["port"] > 0 and node["port"] <= 65535):
                    pass
                else:
                    raise ValueError("Bad Input")
            node_record = NodeEntity(node["name"], node["ip"], node["port"])
            node_repository.create_node(node_record)
            await get_push_queue().put(json.dumps(NodeCreateResultMessage(node_record).__dict__))
            return aiocoap.Message(payload=b"OK", code=aiocoap.Code.CREATED)
        except JSONDecodeError as ex:
            logging.warning("Problem processing request: %s", ex)
        except ValueError as val_ex:
            logging.warning(
                "Bad input. Please correct node ip, node port and node name! Error: %s", val_ex)
        except sqlite3.IntegrityError as integ_ex:
            logging.warning("Duplicate Entry. Can not process.")
        return aiocoap.Message(payload=b"INVALID REQUEST", code=aiocoap.Code.BAD_REQUEST)

    async def render_get(self, request):
        """
        handle GET request to /nodes

        :param request:
        :return:
        """
        # TODO: return a list of all nodes we know
        return aiocoap.Message(payload=b"Node")

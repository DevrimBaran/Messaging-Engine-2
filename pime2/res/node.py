import json
import logging
from json import JSONDecodeError

import aiocoap
from aiocoap import resource

from pime2.message import NodeCreateResultMessage
from pime2.node import NodeEntity
from pime2.push_queue import get_push_queue


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
        required_fields = [
            "name",
            "ip",
            "port",
        ]
        # parse node record from request payload - if possible
        try:
            if len(request.payload) > 2048:
                return aiocoap.Message(payload=b"INVALID REQUEST", code=aiocoap.Code.BAD_REQUEST)
            node = json.loads(request.payload)

            for i in required_fields:
                if i not in node or node[i] is None:
                    return aiocoap.Message(payload=b"INVALID REQUEST, MISSING PROPERTY", code=aiocoap.Code.BAD_REQUEST)
                # TODO: sanitize input
            node_record = NodeEntity(node["name"], node["ip"], node["port"])
            await get_push_queue().put(json.dumps(NodeCreateResultMessage(node_record).__dict__))
            return aiocoap.Message(payload=b"OK", code=aiocoap.Code.CREATED)
        except JSONDecodeError as ex:
            logging.warning("Problem processing request: %s", ex)
        return aiocoap.Message(payload=b"INVALID REQUEST", code=aiocoap.Code.BAD_REQUEST)

    async def render_get(self, request):
        """
        handle GET request to /nodes

        :param request:
        :return:
        """
        # TODO: return a list of all nodes we know
        return aiocoap.Message(payload=b"Node")

import datetime
import json
import logging
from json import JSONDecodeError
from typing import List

import re
from aiocoap import resource, Message, Code

from pime2 import NAME_REGEX, BASE64_REGEX
from pime2.common import base64_decode
from pime2.mapper.flow_mapper import FlowMapper
from pime2.message import FlowMessageResultMessage
from pime2.push_queue import get_push_queue


class FlowMessage(resource.Resource):
    """
    Flow Resource
    """

    async def render_put(self, request):
        """
        handle get request for /flows

        :param request:
        :return:
        """
        response = await self.handle_incoming_flow_message(request)
        logging.info("Flow create request %s", response)
        return response

    async def handle_incoming_flow_message(self, request) -> Message:
        """Handles incoming node request and saves it to the database if everything is valid"""
        if len(request.payload) > 2048:
            return Message(payload=b"INVALID REQUEST", code=Code.BAD_REQUEST)

        try:
            node = json.loads(request.payload)
            logging.debug("received dict on flow-messages endpoint: %s", node)
            is_valid = await self.is_request_valid(dict(node))
            if not is_valid:
                return Message(payload=b"INVALID REQUEST, MISSING OR INVALID PROPERTY", code=Code.BAD_REQUEST)

            flow_message = FlowMapper().json_to_message_entity(node)

            await get_push_queue().put(json.dumps(FlowMessageResultMessage(flow_message).__dict__, default=str))
            return Message(payload=b"OK", code=Code.CREATED)
        except JSONDecodeError as ex:
            logging.warning("Problem encoding request: %s", ex)
        return Message(payload=b"INVALID REQUEST", code=Code.BAD_REQUEST)

    async def is_request_valid(self, node: dict) -> bool:
        """
        Method to check if a given dictionary is a valid flow_message
        :param node:
        :return:
        """
        if isinstance(node, str):
            logging.debug("Invalid json received!")
            return False
        required_fields = [
            "id",
            "flow_name",
            "flow_id",
            "src_created_at",
            "last_operation",
            "next_operation",
            "sent_at",
            "payload",
            "count",
        ]
        for i in required_fields:
            if i not in node or node[i] is None:
                logging.debug("Missing field in flow message: '%s'", i)
                return False
        name_regex_fields = [
            "id",
            "flow_name",
            "flow_id",
            "last_operation",
            "next_operation",
        ]
        for namelike_field in name_regex_fields:
            if not re.match(NAME_REGEX, node[namelike_field]):
                logging.debug("Invalid name like field '%s'", namelike_field)
                return False

        for datetimelike_field in ["src_created_at", "sent_at"]:
            try:
                datetime.datetime.fromisoformat(str(node[datetimelike_field]))
            except ValueError:
                logging.debug("Invalid date in field %s", datetimelike_field)
                return False

        if not isinstance(node["count"], int):
            logging.debug("Invalid integer value for 'count'")
            return False

        if "history" in node and node["history"] is not None and isinstance(node["history"], List):
            for i in node["history"]:
                return await self.is_request_valid(i)

        # check if the payload is a valid base64 string (ascii chars + strlen == 0 mod 4)
        s = str(node["payload"])
        match = re.match(BASE64_REGEX, s)
        if not match:
            logging.debug("Invalid base64 payload received")
            return False

        payload_content = base64_decode(node["payload"])
        try:
            json.loads(payload_content)
        except JSONDecodeError:
            logging.debug("Decoded payload is not a valid JSON")
            return False

        return True

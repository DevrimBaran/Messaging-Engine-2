import aiocoap
import logging
import json
from aiocoap import resource, Message, Code
from json import JSONDecodeError
from pime2.message import FlowCreateResultMessage
from pime2.push_queue import get_push_queue
from pime2.service.flow_service import FlowService
from pime2.mapper.flow_mapper import FlowMapper


class Flow(resource.Resource):
    """
    Flow Resource
    """

    def __init__(self):
        self.flow_service = FlowService()
        self.flow_mapper = FlowMapper()

    async def render_get(self, request):
        """
        handle get request for /flows

        :param request:
        :return:
        """
        flow_list_json = self.flow_service.get_all_flows_as_json()
        logging.info("Response JSON: %s", flow_list_json)
        return aiocoap.Message(payload=flow_list_json.encode())


    async def render_put(self, request):
        """
        handle get request for /flows

        :param request:
        :return:
        """

        response = await self.handle_incoming_flow(request)
        logging.info("Flow create response: %s", response)
        return response


    async def handle_incoming_flow(self, request) -> Message:
        """Handles incoming node request and saves it to the database if everything is valid"""
        try:
            is_valid = await self.is_request_valid(request)
            if not is_valid:
                return Message(payload=b"INVALID REQUEST, MISSING OR INVALID PROPERTY", code=Code.BAD_REQUEST)
            flow_json = request.payload.decode()
            flow_entity = self.flow_mapper.json_to_flow_entity(flow_json)
            self.flow_service.put_flow(flow_entity)
            #TODO in push queue
            #await get_push_queue().put(FlowCreateResultMessage(flow_entity))
            return Message(payload=b"OK", code=Code.CREATED)
        except JSONDecodeError as ex:
            logging.warning("Problem encoding request: %s", ex)
        return Message(payload=b"INVALID REQUEST", code=Code.BAD_REQUEST)

    async def is_request_valid(self, request) -> bool:
        """Validate the payload of the request whether it fits the specifications"""
        # TODO: validate pime2.flow.flow_validation_service.FlowValidationService.is_flow_valid
        return True

import logging
from aiocoap import resource, Message
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
        response = await self.node_service.handle_incoming_node(request)
        logging.info("Response: %s", response)
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

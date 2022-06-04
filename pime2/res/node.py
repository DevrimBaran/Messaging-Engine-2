import logging
from aiocoap import resource, Message
from pime2.service.node_service import NodeService
from pime2.database import get_db_connection
class Node(resource.Resource):
    """
    Node Resource
    """

    def __init__(self):
        self.node_service = NodeService(get_db_connection())

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

    async def render_delete(self, request):
        """
        handle DELETE request to /nodes
        Deletes all nodes from the database

        :param request:
        :return:
        """
        self.node_service.delete_all_nodes()
        return Message(payload=b'Deleted all nodes')

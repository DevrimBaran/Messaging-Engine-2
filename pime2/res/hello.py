import aiocoap
from aiocoap import resource
from pime2.repository.NodeRepository import NodeRepository
from pime2.service.NodeService import NodeService
from aiocoap import Code, Message


class Hello(resource.Resource):
    """
    Hello Resource
    """
    def __init__(self):
        self.node_service = NodeService()

    async def render_put(self, request):
        """Handles incoming hello message and sends own node entity json as a response"""
        handle_node_message = await self.node_service.handle_incoming_node(request)
        if handle_node_message.code == Code.CREATED:
            my_node = self.node_service.get_own_node()
            my_node_json = self.node_service.entity_to_json(my_node)
            return Message(payload=my_node_json.encode())
        else:
            return handle_node_message

    async def render_get(self, request):
        """
        handle GET request to /hello

        :param request:
        :return:
        """
        return Message(payload=b"Helloooo!")

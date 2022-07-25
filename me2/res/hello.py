import aiocoap
from aiocoap import resource, Message
from me2.service.node_service import NodeService


class Hello(resource.Resource):
    """
    Hello Resource
    """

    def __init__(self):
        self.node_service: NodeService = NodeService()

    async def render_get(self, request):
        """
        handle GET request to /hello

        :param request:
        :return:
        """
        own_node = self.node_service.get_own_node()
        if own_node is not None:
            own_node_json = self.node_service.entity_to_json(own_node)
            return Message(payload=own_node_json.encode())
        return Message(payload="Problem fetching own node".encode(), code=aiocoap.Code.INTERNAL_SERVER_ERROR)

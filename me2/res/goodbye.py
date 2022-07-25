from aiocoap import resource, Code, Message
from me2.service.node_service import NodeService


class Goodbye(resource.Resource):
    """
    Goodbye Resource
    """

    def __init__(self):
        self.node_service = NodeService()

    async def render_delete(self, request):
        """handles incoming goodbye message"""
        self.node_service.remove_node(request.payload.decode())
        return Message(payload=b"Goodbye", code=Code.DELETED)

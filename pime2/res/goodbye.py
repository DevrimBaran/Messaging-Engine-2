from aiocoap import resource, Code, Message
from pime2.service.node_service import NodeService
from pime2.database import get_db_connection

class Goodbye(resource.Resource):
    """
    Goodbye Resource
    """

    def __init__(self):
        self.node_service = NodeService(get_db_connection)

    async def render_delete(self, request):
        """handles incoming goodbye message"""
        self.node_service.remove_node(request.payload.decode())
        return Message(payload=b"Goodbye", code=Code.DELETED)

import json
from aiocoap import resource, Message
from pime2.service.node_service import NodeService
from pime2.database import get_db_connection



class Hello(resource.Resource):
    """
    Hello Resource
    """
    def __init__(self):
        self.node_service = NodeService(get_db_connection())

    async def render_get(self, request):
        """
        handle GET request to /hello

        :param request:
        :return:
        """
        own_node = self.node_service.get_own_node()
        own_node_json = json.dumps(own_node.__dict__)
        return Message(payload=own_node_json.encode())

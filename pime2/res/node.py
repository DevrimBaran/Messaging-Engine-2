import aiocoap
from aiocoap import resource


class Node(resource.Resource):
    """
    Node Resource
    """

    async def render_get(self, request):
        """
        handle GET request to /nodes

        :param request:
        :return:
        """
        return aiocoap.Message(payload=b"Node")

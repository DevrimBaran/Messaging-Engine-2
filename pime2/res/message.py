import aiocoap
from aiocoap import resource


class Message(resource.Resource):
    """
    Message Resource
    """

    async def render_get(self, request):
        """
        handle GET request to /messages

        :param request:
        :return:
        """
        return aiocoap.Message(payload=b"Message")

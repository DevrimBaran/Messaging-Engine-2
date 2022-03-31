import aiocoap
from aiocoap import resource


class Hello(resource.Resource):
    """
    Hello Resource
    """

    async def render_get(self, request):
        """
        handle GET request to /hello

        :param request:
        :return:
        """
        return aiocoap.Message(payload=b"Helloooo!")

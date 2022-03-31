import aiocoap
from aiocoap import resource


class Health(resource.Resource):
    """
    Health Resource
    """

    async def render_get(self, request):
        """
        handle GET request to /health

        :param request:
        :return:
        """
        return aiocoap.Message(payload=b"Health")

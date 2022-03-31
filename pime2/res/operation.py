import aiocoap
from aiocoap import resource


class Operation(resource.Resource):
    """
    Operation Resource
    """

    async def render_get(self, request):
        """
        handle GET request to /operations

        :param request:
        :return:
        """
        return aiocoap.Message(payload=b"Operation")

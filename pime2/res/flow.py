import aiocoap
from aiocoap import resource


class Flow(resource.Resource):
    """
    Flow Resource
    """

    async def render_get(self, request):
        """
        handle get request for /flows

        :param request:
        :return:
        """
        return aiocoap.Message(payload=b"Flow")

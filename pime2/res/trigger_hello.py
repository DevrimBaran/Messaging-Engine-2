import aiocoap
from aiocoap import resource


class TriggerHello(resource.Resource):
    """
    Trigger-Hello Resource
    """

    async def render_get(self, request):
        """
        handle GET request to /trigger-hello

        :param request:
        :return:
        """
        return aiocoap.Message(payload=b"Trigger Hello!")

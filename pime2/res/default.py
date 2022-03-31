import aiocoap
from aiocoap import resource


class Default(resource.Resource):
    """
    default = NOT_FOUND
    """

    async def render_get(self, request):
        """
        default handling = returning NOT_FOUND

        :param request:
        :return:
        """
        return aiocoap.Message(payload=b"Default", code=aiocoap.Code.NOT_FOUND)

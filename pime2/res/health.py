import json
import os
import aiocoap
import psutil
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

        pime_version = "0.0.1"
        cpu_core_count = os.cpu_count()
        cpu_usage = psutil.cpu_percent()
        ram_availabe = psutil.virtual_memory().available
        ram_used = psutil.virtual_memory().used
        ram_used_percentage = psutil.virtual_memory().percent
        neighbour_count = 0
        sensor_count = 0
        actuator_count = 0

        response_dict = {
            "version": pime_version,
            "cpu_core_count": cpu_core_count,
            "cpu_usage": cpu_usage,
            "ram_available": ram_availabe,
            "ram_used": ram_used,
            "ram_used_percentage": ram_used_percentage,
            "neighbour_count": neighbour_count,
            "sensor_count": sensor_count,
            "actuator_count": actuator_count
        }

        response_json = json.dumps(response_dict)

        return aiocoap.Message(payload=response_json.encode())

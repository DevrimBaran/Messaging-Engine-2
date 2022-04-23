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
            "PIME version": pime_version,
            "CPU core count": cpu_core_count,
            "CPU usage": cpu_usage,
            "RAM available": ram_availabe,
            "RAM used": ram_used,
            "RAM used Percentage": ram_used_percentage,
            "Neighbour count": neighbour_count,
            "Sensor count": sensor_count,
            "Actuator count": actuator_count
        }

        response_json = json.dumps(response_dict)

        return aiocoap.Message(payload=response_json.encode())

import json
import os
import aiocoap
import psutil
from aiocoap import resource

from me2.service.node_service import NodeService


class Health(resource.Resource):
    """
    Health Resource
    """

    def __init__(self) -> None:
        """
        Constructor method, initialize node service
        """
        self.node_service = NodeService()

    async def render_get(self, request):
        """
        handle GET request to /health

        :param request:
        :return:
        """
        own_node = self.node_service.get_own_node()
        cpu_core_count = os.cpu_count()
        cpu_usage = psutil.cpu_percent()
        ram_total = psutil.virtual_memory().total
        ram_availabe = psutil.virtual_memory().available
        ram_used = psutil.virtual_memory().used
        ram_used_percentage = psutil.virtual_memory().percent
        neighbor_count = len(self.node_service.get_all_neighbor_nodes())
        sensor_count = len(own_node.sensor_skills)
        actuator_count = len(own_node.actuator_skills)

        response_dict = {
            "cpu_core_count": cpu_core_count,
            "cpu_usage": cpu_usage,
            "ram_total" : ram_total,
            "ram_available": ram_availabe,
            "ram_used": ram_used,
            "ram_used_percentage": ram_used_percentage,
            "neighbor_count": neighbor_count,
            "sensor_count": sensor_count,
            "actuator_count": actuator_count
        }

        response_json = json.dumps(response_dict)

        return aiocoap.Message(payload=response_json.encode())

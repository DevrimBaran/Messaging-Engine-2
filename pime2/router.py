import json
import logging

from pime2.flow import FlowManager
from pime2.message import MessageType
from pime2.sensor.sensor import SensorType
from pime2.service.node_service import NodeService


async def router_loop(msg, manager: FlowManager):
    """
    This method is called whenever an internal message is processed.
    It basically decides which method needs to be called for which incoming message (type).

    :param manager:
    :param msg:
    :return:
    """
    received_object = json.loads(msg[0])
    logging.info("received message json: %s", received_object)
    if "message_type" in received_object and received_object["message_type"] is not None:
        message_type = received_object["message_type"]
        if message_type == MessageType.SENSOR_RESULT.value:
            if "sensor_type" in received_object:
                sensor_type = received_object["sensor_type"]
                sensor_flows = manager.get_available_flows_for_sensor(sensor_type)
                for i in sensor_flows:
                    await manager.start_flow(i, received_object["message_content"])

            logging.debug("detected sensor_read for sensor %s", SensorType(received_object["sensor_type"]))
        elif message_type == MessageType.NODE_CREATE.value:
            NodeService().put_node(json.dumps(received_object["message_content"]))
            logging.debug("detected node create event with node: %s", received_object["message_content"])
    else:
        logging.error("problem with received message: %s", received_object)

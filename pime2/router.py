import json
import logging

from sqlite3 import IntegrityError
from pime2.message import MessageType
from pime2.sensor.sensor import SensorType
from pime2.service.node_service import NodeService


async def router_loop(msg):
    """
    This method is called whenever an internal message is processed.
    It basically decides which method needs to be called for which incoming message (type).

    :param msg:
    :return:
    """
    received_object = json.loads(msg[0])
    if "message_type" in received_object and received_object["message_type"] is not None:
        message_type = received_object["message_type"]
        if message_type == MessageType.SENSOR_RESULT.value:
            logging.debug("detected sensor_read for sensor %s", SensorType(received_object["sensor_type"]))
        elif message_type == MessageType.NODE_CREATE.value:
            NodeService().put_node(json.dumps(received_object["message_content"]))
            logging.debug("detected node create event with node: %s", received_object["message_content"])
        logging.info("received message json: %s", received_object)
    else:
        logging.error("problem with received message: %s", received_object)

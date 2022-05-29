import json
import logging

from sqlite3 import IntegrityError
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

    # "message_type" and "message_content" are required here
    if "message_type" in received_object and "message_content" in received_object \
            and received_object["message_type"] is not None and received_object["message_content"] is not None:
        message_type = received_object["message_type"]
        if message_type == MessageType.SENSOR_RESULT.value:
            if "sensor_type" in received_object:
                sensor_type = received_object["sensor_type"]
                # TODO use sensor_type as string not int value for enum
                sensor_flows = manager.get_available_flows_for_sensor(sensor_type)
                for i in sensor_flows:
                    manager.start_flow(i, received_object["message_content"])

            logging.debug("detected sensor_read for sensor %s", SensorType(received_object["sensor_type"]))
        elif message_type == MessageType.NODE_CREATE.value:
            node_service = NodeService()
            node = json.dumps(received_object["message_content"])
            try:
                node_service.put_node(node)
            except IntegrityError:
                logging.debug("Duplicate Entry")
            else:
                logging.debug("detected node create event with node: %s", node)
        logging.info("received message json: %s", received_object)
    else:
        logging.error("problem with received message: %s", received_object)

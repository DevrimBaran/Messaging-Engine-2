import json
import logging

from pime2.flow.flow_manager import FlowManager
from pime2.mapper.flow_mapper import FlowMapper
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
    logging.debug("Received message json: %s", received_object)

    # "message_type" and "message_content" are required here
    if "message_type" in received_object and "message_content" in received_object \
            and received_object["message_type"] is not None and received_object["message_content"] is not None:
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
        elif message_type == MessageType.FLOW_MESSAGE.value:
            flow_message = received_object["message_content"]

            if "flow_name" not in flow_message:
                logging.error("Invalid FlowMessage object received!")
                return

            selected_flow = list(filter(lambda x: x.name == flow_message["flow_name"], manager.get_flows()))
            if len(selected_flow) < 1:
                logging.error(
                    "PROBLEM: Invalid FlowMessage object received! Cannot find flow: '%s' FlowMessage is skipped",
                    flow_message["flow_name"])
                return
            if len(selected_flow) > 1:
                logging.error("PROBLEM: Multiple flows with the same name found! FlowMessage is skipped")
                return
            await manager.execute_flow(selected_flow[0], FlowMapper().json_to_message_entity(flow_message),
                                       manager.get_nodes())

    else:
        logging.error("Problem with received message: %s", received_object)

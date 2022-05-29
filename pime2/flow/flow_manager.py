import logging
from typing import List

from pime2.flow.flow_message_builder import FlowMessageBuilder
from pime2.flow.flow_operation_manager import FlowOperationManager
from pime2.flow.flow_validation_service import FlowValidationService
from pime2.entity import FlowEntity, FlowOperationEntity, FlowMessageEntity, NodeEntity
from pime2.sensor.sensor import SensorType
from pime2.service.node_service import NodeService


class FlowManager:
    """
    This class encapsulates logic around processing and handling flows.
    Flow step operations are executed by FlowOperationManager.
    """

    def __init__(self, flow_validation_service: FlowValidationService,
                 flow_operation_manager: FlowOperationManager,
                 flow_message_builder: FlowMessageBuilder,
                 node_service: NodeService):
        self.flow_validation_service = flow_validation_service
        self.flow_operation_manager = flow_operation_manager
        self.flow_message_builder = flow_message_builder
        self.node_service = node_service

    def get_nodes(self) -> List[NodeEntity]:
        """
        This methods provides a list of currently known nodes.
        FIXME: This method will be replaced with a db access in a later step.

        :return:
        """
        return [
            NodeEntity("instance_1", "10.10.10.1", 5683),
            NodeEntity("instance_2", "10.10.10.2", 5683),
        ]

    def get_flows(self) -> List[FlowEntity]:
        """
        This methods provides a list of currently known nodes.
        FIXME: This method will be replaced with a db access in a later step.

        :return:
        """
        flow_ops = [FlowOperationEntity("op_name", "sensor_read_temperature", None, None, "*"),
                    FlowOperationEntity("op_name2", None, "log", None, "*")]
        flow = FlowEntity("test_flow", flow_ops)
        return [
            flow,
        ]

    def start_flow(self, flow: FlowEntity, result: dict):
        # validate
        is_valid, validation_msgs = self.flow_validation_service.is_flow_valid(flow)
        if not is_valid:
            logging.error(f"Problem with flow '{flow.name}'")
            for i in validation_msgs:
                logging.error(f"Validation message: {i}")
            return

        # detect next step
        step = self.flow_operation_manager.detect_second_step(flow)
        if step is None:
            logging.error(f"Could not detect second step of flow: {flow.name}")
            return
        # detect nodes of next step and send new flow message
        nodes = self.flow_operation_manager.detect_nodes_of_step(flow, step)

        if nodes is None or len(nodes) == 0:
            logging.error("No nodes can be found for the next flow operation. Cancelling flow.")
            return

        # build flow message
        msg = self.flow_message_builder.build_start_message(flow, step, result)

        # delegate next step
        for neighbor in nodes:
            if self.node_service.is_node_remote(neighbor):
                self.send_flow_message(msg, neighbor)
            else:
                self.execute_flow(flow, msg)

    def execute_flow(self, flow: FlowEntity, flow_message: FlowMessageEntity):
        # validate
        is_valid, validation_msgs = self.flow_validation_service.is_flow_valid(flow)
        if not is_valid:
            logging.error("Problem with flow '%s'")
            for i in validation_msgs:
                logging.error("Validation message: '%s'", i)
            return

        # detect current step and execute
        current_step = self.flow_operation_manager.detect_current_step(flow, flow_message)
        if current_step is None:
            logging.error("Problem detecting current step of flow '%s'", flow.name)
            return
        if self.flow_operation_manager.is_last_step(flow, current_step):
            return self.finish_flow(flow_message)

        result = self.flow_operation_manager.execute_operation(flow, flow_message, current_step)

        # detect next step and delegate
        step = self.flow_operation_manager.detect_next_step(flow, flow_message)
        if step is None:
            logging.error(f"Could not detect second step of flow: {flow.name}")
            return
        # detect nodes of next step and send new flow message
        nodes = self.flow_operation_manager.detect_nodes_of_step(flow, step)
        if nodes is None or len(nodes) == 0:
            logging.error("No nodes can be found for the next flow operation. Cancelling flow.")
            return

        # build flow message
        next_msg = self.flow_message_builder.build_next_message(flow_message, result)

        # delegate next step
        for neighbor in nodes:
            if self.node_service.is_node_remote(neighbor):
                self.send_flow_message(next_msg, neighbor)
            else:
                self.execute_flow(flow, next_msg)

    def finish_flow(self, flow: FlowEntity, flow_message: FlowMessageEntity):
        # validate
        is_valid, validation_msgs = self.flow_validation_service.is_flow_valid(flow)
        if not is_valid:
            logging.error("Problem with flow '%s'")
            for i in validation_msgs:
                logging.error("Validation message: '%s'", i)
            return

        # detect current step and execute
        final_step = self.flow_operation_manager.detect_current_step(flow, flow_message)
        if final_step is None:
            logging.error("Problem detecting current step of flow '%s'", flow.name)
            return
        # TODO: Check if this is really the last step

        step_result = self.flow_operation_manager.execute_operation(flow, flow_message, final_step)
        logging.info("Finished flow")
        return

    def send_flow_message(self, flow_message: FlowMessageEntity, node: NodeEntity):
        logging.info("Send FlowMessage to %s:%s", node.ip, node.port)
        # TODO implement CoAp-Client logic here

    def get_available_flows_for_sensor(self, sensor_type: SensorType) -> List[FlowEntity]:
        # TODO implement
        return self.get_flows()

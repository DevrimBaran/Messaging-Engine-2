import logging
from typing import List

from pime2.config import get_me_conf
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
        self.startup()

    def get_nodes(self) -> List[NodeEntity]:
        """
        This methods provides a list of currently known nodes.
        FIXME: This method will be replaced with a db access in a later step.

        :return:
        """
        return self.node_service.get_all_nodes()

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

    def start_flow(self, flow: FlowEntity, sensor_type: SensorType, result: dict):
        neighbors = self.get_nodes()

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
        nodes = self.flow_operation_manager.detect_nodes_of_step(flow, step, neighbors)

        if nodes is None or len(nodes) == 0:
            logging.error("No nodes can be found for the next flow operation. Cancelling flow.")
            return

        # build flow message
        msg = self.flow_message_builder.build_start_message(flow, step, result)
        # and send message to nodes
        self.send_message_to_nodes(flow, msg, nodes)

    def execute_flow(self, flow: FlowEntity, flow_message: FlowMessageEntity, neighbors: List[NodeEntity]):
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
            return self.finish_flow(flow, flow_message)

        is_done = self.execute_step(flow, flow_message, current_step, neighbors)
        if not is_done:
            logging.info("Flow is not executed locally.")
            return

        # detect next step and delegate
        next_step = self.flow_operation_manager.detect_next_step(flow, flow_message)
        if next_step is None:
            logging.error(f"Could not detect second step of flow: {flow.name}")
            return
        # detect nodes of next step and send new flow message
        nodes = self.flow_operation_manager.detect_nodes_of_step(flow, next_step, neighbors)
        if nodes is None or len(nodes) == 0:
            logging.error("No nodes can be found for the next flow operation. Cancelling flow.")
            return

        # build flow message
        next_msg = self.flow_message_builder.build_next_message(flow, flow_message, result, current_step, next_step)

        self.send_message_to_nodes(flow, next_msg, nodes)

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

    def startup(self):
        """
        This method is called at the end of the constructor to do prepare the flow managers work.
        :return:
        """
        node = self.node_service.get_own_node()
        if node is None:
            # Create own entry
            logging.info("FlowManager: Creating self node")
            me_conf = get_me_conf()
            self.node_service.put_node(NodeEntity(me_conf.instance_id, me_conf.host, me_conf.port))
        else:
            logging.info("FlowManager: Self node exists")

    def execute_step(self, flow: FlowEntity, flow_message: FlowMessageEntity, step: str,
                     nodes: List[NodeEntity]) -> bool:
        """
        Helper method to execute a single step locally and remote.
        If the execution was also locally, the return value is true, else false.
        :param flow:
        :param flow_message:
        :param step:
        :param nodes:
        :return:
        """
        nodes_of_step = self.flow_operation_manager.detect_nodes_of_step(flow, step, nodes)

        message = self.flow_message_builder.build_redirection_message(flow_message)
        for node in nodes_of_step:
            if self.node_service.is_node_remote(node):
                self.send_flow_message(message, node)

        is_executed_locally = len(list(filter(lambda x: x.name == get_me_conf().instance_id, nodes_of_step))) > 0
        if is_executed_locally:
            self.flow_operation_manager.execute_operation(flow, flow_message, step)
            return True
        return False

    def send_message_to_nodes(self, flow: FlowEntity, message: FlowMessageEntity, nodes: List[NodeEntity]):
        for neighbor in nodes:
            if self.node_service.is_node_remote(neighbor):
                self.send_flow_message(message, neighbor)
            else:
                self.execute_flow(flow, message, nodes)

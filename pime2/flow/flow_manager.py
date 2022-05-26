from typing import List

from pime2.flow.flow_operation_manager import FlowOperationManager
from pime2.flow.flow_validation_service import FlowValidationService
from pime2.entity import FlowEntity, FlowOperationEntity, FlowMessageEntity
from pime2.node import NodeEntity


class FlowManager:

    def __init__(self, flow_validation_service: FlowValidationService,
                 flow_operation_manager: FlowOperationManager):
        self.flow_validation_service = flow_validation_service
        self.flow_operation_manager = flow_operation_manager

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

    def get_flow(self) -> List[FlowEntity]:
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

    def start_flow(self, flow: FlowEntity, result):
        pass

    def execute_flow(self, flow: FlowEntity, flow_message: FlowMessageEntity):
        pass

    def finish_flow(self, flow_message: FlowMessageEntity):
        pass

    def send_flow_message(self, flow_message: FlowMessageEntity, node: NodeEntity):
        pass

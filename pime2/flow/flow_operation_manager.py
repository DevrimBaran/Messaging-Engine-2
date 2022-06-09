import json
import logging
from typing import List, Optional

from pime2.actuator.actuator import ActuatorType
from pime2.actuator.actuator_manager import ActuatorManager
from pime2.common import base64_decode
from pime2.entity import FlowEntity, NodeEntity, FlowMessageEntity


class FlowOperationManager:
    """
    This class handles the execution of a single flow operation step.
    You should make sure the flow is validated before using the following methods.

    """

    @staticmethod
    def detect_current_step(flow: FlowEntity, flow_message: FlowMessageEntity) -> Optional[str]:
        """
        Method to detect the current operation: it is the next after the last

        :param flow:
        :param flow_message:
        :return:
        """
        if flow_message.flow_name != flow.name:
            return None
        for f in flow.ops:
            if f.name.lower() == flow_message.last_operation.lower():
                return FlowOperationManager.detect_next_step(flow, flow_message.last_operation)
        return None

    @staticmethod
    def detect_next_step(flow: FlowEntity, current_step: str) -> Optional[str]:
        """
        Detect next step

        :param flow:
        :param current_step:
        :return:
        """
        take_this = False
        i = 0
        for f in flow.ops:
            i += 1
            if take_this:
                return f.name
            if f.name.lower() == current_step.lower():
                # return next or last
                take_this = True
                if len(flow.ops) == i:
                    return f.name
        return None

    @staticmethod
    def detect_second_step(flow: FlowEntity) -> Optional[str]:
        """
        Returns the name of the second flow of the given entity.

        :param flow:
        :return:
        """
        if len(flow.ops) <= 1:
            return None
        return flow.ops[1].name

    @staticmethod
    def detect_nodes_of_step(flow: FlowEntity, step: str, nodes: List[NodeEntity]) -> List[NodeEntity]:
        """
        Method to detect which nodes are affected by the given step.
        TODO: Consider skills here (ME-44?)

        :param flow:
        :param step:
        :param nodes:
        :return:
        """
        if len(flow.ops) == 0:
            logging.warning("Got flow without operations!")
            return []

        for f in flow.ops:
            if f.name.lower() == step.lower():
                where_clause = f.where.strip()
                if where_clause == "*":
                    return nodes
                node_list = []
                for name in where_clause.split(","):
                    for node in nodes:
                        if node.name == name.strip():
                            node_list.append(node)
                return node_list

        return []

    @staticmethod
    async def execute_operation(flow: FlowEntity, flow_message: FlowMessageEntity, step: str) -> Optional[str]:
        """
        Method to execute an operation of a flow message defined by the step.
        The returned str is the base64 encoded output value of this operation, and it is the payload
        for the next flow message.

        :param flow:
        :param flow_message:
        :param step:
        :return: Optional[Dict]
        """
        if flow_message.flow_name != flow.name:
            logging.warning("Invalid flow_message for flow received. Invalid names: flow: %s, flow message: %s",
                            flow.name, flow_message.flow_name)
            return None
        is_executed = False
        for f in flow.ops:
            if f.name.lower() == step.lower():
                flow_operation_name = f.name.lower()
                flow_operation = f.process
                is_executed = True

                payload = base64_decode(flow_message.payload)
                logging.info("EXECUTE OPERATION %s:%s with input: %s", flow_operation_name,
                             flow_operation, payload)

                if f.is_process():
                    if f.process == "cep_operation":
                        # TODO: execute cep operation
                        pass
                    if f.process == "log":
                        logging.info("LOG OPERATION: %s", json.loads(payload))

                if f.is_output():
                    manager = ActuatorManager()
                    if f.output == "actuator_led":
                        manager.one_time_trigger(ActuatorType.LED)
                    if f.output == "actuator_speaker":
                        manager.one_time_trigger(ActuatorType.SPEAKER)

                return flow_message.payload
        if not is_executed:
            logging.error("No operation executed in flow %s with step %s", flow.name, step)
        return None

    @staticmethod
    def is_last_step(flow: FlowEntity, current_step: str) -> bool:
        """"
        This method detects if a step is the last one in a flow
        """
        if len(flow.ops) == 0:
            logging.warning("Got flow without operations!")
            return False

        total = len(flow.ops)
        i = 0
        for f in flow.ops:
            i += 1
            if f.name.lower() == current_step.lower() and i == total:
                return True
        return False

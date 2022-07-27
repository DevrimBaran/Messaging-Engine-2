import json
import logging
from typing import List, Optional

from pime2.actuator.actuator import ActuatorType
from pime2.actuator.actuator_manager import ActuatorManager
from pime2.common import base64_decode
from pime2.entity import FlowEntity, NodeEntity, FlowMessageEntity
from pime2.flow.filter_flow import filter_executer
from pime2.repository.execution_repository import ExecutionRepository


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
    async def execute_operation(flow: FlowEntity, flow_message: FlowMessageEntity, step: str,
                                execution_repository: ExecutionRepository) -> Optional[str]:
        """
        Method to execute an operation of a flow message defined by the step.
        The returned str is the base64 encoded output value of this operation, and it is the payload
        for the next flow message.

        :param execution_repository:
        :param flow:
        :param flow_message:
        :param step:
        :return: Optional[Dict]
        """
        if flow_message.flow_name != flow.name:
            logging.warning("Invalid flow_message for flow received. Invalid names: flow: %s, flow message: %s",
                            flow.name, flow_message.flow_name)
            return None

        logging.debug("Execute operation '%s' for flow '%s' (%s)", step, flow.name, flow)
        for f in flow.ops:
            if f.name.lower() == step.lower():
                flow_operation_name = f.name.lower()
                flow_operation = f.process

                was_executed_before, executed_at = execution_repository.is_message_executed(flow_message.flow_id,
                                                                                            flow_message.id)
                if was_executed_before:
                    # prevent duplicate operation execution
                    logging.error(
                        "DUPLICATE FLOW OPERATION PREVENTED! %s:%s, message_id: %s flow_id: %s, executed at %s",
                        flow_operation_name, flow_operation,
                        flow_message.id, flow_message.flow_id, executed_at)
                else:
                    # first execution
                    payload = base64_decode(flow_message.payload)
                    logging.info("EXECUTE OPERATION %s:%s with input: %s", flow_operation_name,
                                 flow_operation, payload)
                    execution_repository.register_execution(flow_message.flow_id, flow_message.id)

                    if f.is_process():
                        if f.process == "filter_intercept":
                            if not isinstance(f.args, dict) or \
                               "expression" not in f.args or f.args["expression"] is None or \
                               "variables" not in f.args or f.args["variables"] is None:
                                logging.error("Stopping flow: expression or variables are not defined")
                                return None
                            logging.info("Executing filter evaluation in flow %s with step %s", flow.name, step)
                            if not filter_executer(f.args["expression"], f.args["variables"], payload):
                                logging.info("Stopping flow: filter evaluation returned false")
                                return None
                        if f.process == "log":
                            logging.info("LOG OPERATION: %s", json.loads(payload))

                    if f.is_output():
                        manager = ActuatorManager()
                        if f.output == "actuator_led":
                            manager.one_time_trigger(ActuatorType.LED)
                        if f.output == "actuator_speaker":
                            manager.one_time_trigger(ActuatorType.SPEAKER)
                return flow_message.payload

        logging.error("No operation executed in flow %s with step %s", flow.name, step)
        return flow_message.payload

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

    @staticmethod
    def is_filter_operation(flow: FlowEntity, step: str) -> bool:
        """method to check if a single flow operation is the filter operation or not"""
        for op in flow.ops:
            if op.name.lower() == step.lower():
                if op.process.lower() == "filter_intercept":
                    return True
        return False

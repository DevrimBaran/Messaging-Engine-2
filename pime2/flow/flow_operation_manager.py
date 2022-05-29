import logging
from typing import List, Optional

from pime2.entity import FlowEntity, NodeEntity, FlowMessageEntity


class FlowOperationManager:
    """
    This class handles the execution of a single flow operation step.

    """

    def detect_current_step(self, flow: FlowEntity, flow_message: FlowMessageEntity) -> Optional[str]:
        """
        Method to read the "next_operation"

        :param flow:
        :param flow_message:
        :return:
        """
        if flow_message.flow_name != flow.name:
            return None
        for f in flow.ops:
            if f.name.lower() == flow_message.next_operation.lower():
                return f.name
        return None

    def detect_next_step(self, flow: FlowEntity, flow_message: FlowMessageEntity) -> Optional[str]:
        """
        Detect next step

        :param flow:
        :param flow_message:
        :return:
        """
        if flow_message.flow_name != flow.name:
            return None
        take_this = False
        for f in flow.ops:
            if take_this:
                return f.name
            if f.name.lower() == flow_message.next_operation.lower():
                take_this = True
        return None

    def detect_second_step(self, flow: FlowEntity) -> Optional[str]:
        """
        Returns the name of the second flow of the given entity.

        :param flow:
        :return:
        """
        if len(flow.ops) <= 1:
            return None
        return flow.ops[1].name

    def detect_nodes_of_step(self, flow: FlowEntity, step: str, nodes: List[NodeEntity]) -> List[NodeEntity]:
        """
        Method to detect which nodes are affected by the given step.
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
                        if node.name == name:
                            node_list.append(node)
                return node_list

        return []

    def execute_operation(self, flow: FlowEntity, flow_message: FlowMessageEntity, step: str):
        """
        Method to execute an operation of a flow message defined by the step

        :param flow:
        :param flow_message:
        :param step:
        :return:
        """
        if flow_message.flow_name != flow.name:
            logging.warning("Invalid flow_message for flow received. Invalid names: flow: %s, flow message: %s",
                            flow.name, flow_message.flow_name)
            return None
        is_executed = False
        for f in flow.ops:
            if f.name.lower() == step.lower():
                flow_operation_name = f.name.lower()
                is_executed = True
                logging.info("FlowOperationManager: EXECUTE OPERATION %s:%s with input: %s", flow_operation_name,
                             f.process, flow_message.payload)
                # TODO: execute operation
        if not is_executed:
            logging.error("FlowOperationManager: No operation executed in flow %s with step %s", flow.name, step)
        return None

    def is_last_step(self, flow: FlowEntity, current_step: str) -> bool:
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

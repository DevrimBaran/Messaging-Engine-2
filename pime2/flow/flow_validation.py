# pylint: disable=too-many-return-statements,too-many-locals
import logging
import re
from operator import xor

from pime2 import NAME_REGEX
from pime2.entity import FlowEntity
from pime2.flow.flow_operation_manager import FlowOperationManager
from pime2.service.node_service import NodeService


def is_flow_valid(flow: FlowEntity) -> (bool, str):
    """
    Method to check if a flow is valid.

    :param flow:
    :return:
    """
    pattern = re.compile(NAME_REGEX)
    count_input = 0
    if_input_defined = 0
    if_output_defined = 0
    input_ops = ["sensor_temperature", "sensor_hall", "sensor_button"]
    process_ops = ["log", "cep_intercept"]
    output_ops = ["exit", "actuator_led", "actuator_speaker"]
    op_names = []
    if len(flow.ops) == 0:
        return False, "Got flow without operations!"
    if not re.match(pattern, flow.name):
        return False, f"Flow Name should match following regex: {NAME_REGEX}"
    if len(flow.ops) <= 1:
        return False, "Got flow with too less operations!"
    for op in flow.ops:
        process_exists = 0
        input_exists = 0
        output_exists = 0
        if op.name:
            op_names.append(op.name)
        if op.input not in input_ops and op.input:
            return False, "Wrong input operation!"
        if op.input is not None:
            count_input += 1
            if_input_defined = 1
            input_exists = 1
            if count_input > 1:
                return False, "Only one input is allowed in a flow!"
        if op.process is not None:
            process_exists = 1
        if op.process not in process_ops and op.process:
            return False, "Wrong input for process-operation!"
        if not re.match(pattern, op.name):
            return False, f"Operation Name should match following regex: {NAME_REGEX}"
        if op.output is not None:
            if_output_defined = 1
            output_exists = 1
        if op.output not in output_ops and op.output:
            return False, "Wrong input for output-operation!"
        # if len(operation_manager.detect_nodes_of_step(flow, op.name, node_service.get_all_nodes())) == 0:
        #     return False, "Can not execute node step execution!"
        if xor(xor(output_exists, input_exists), process_exists) != 1:
            return False, "Only one of the following types are allowed per flow: 'input', 'process', 'output'!"
    if not if_output_defined:
        return False, "No output defined!"
    if not if_input_defined:
        return False, "No input defined!"
    op_names_set = set(op_names)
    if len(op_names_set) != len(op_names):
        return False, "Operation names need to be unique per flow!"
    return True, ""


def is_flow_step_executable(flow: FlowEntity, step: str, node_service: NodeService) -> bool:
    """
    Checks: Are there nodes for all operations of the flow?
    """
    for op in flow.ops:
        if op.name.lower() == step.lower():
            if op.is_input():
                if not node_service.get_own_node().has_skill(op.input):
                    logging.debug("No sensor skill '%s' known", op.input)
                    return False
            else:
                if op.is_output() and op.output.strip().lower() != "exit" \
                        and not node_service.get_own_node().has_skill(op.output):
                    # "exit" output operation is allowed on all me 2
                    logging.debug("No actuator skill '%s' known", op.output)
                    return False

            if len(FlowOperationManager.detect_nodes_of_step(flow, op.name, node_service.get_all_nodes())) == 0:
                logging.debug("No executable node found for operation name '%s'", op.name)
                return False
    return True

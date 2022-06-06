import re
from typing import List

from pime2.entity import FlowEntity
from pime2.flow.flow_operation_manager import FlowOperationManager
from pime2.service.node_service import NodeService


def is_flow_valid(flow: FlowEntity) -> (bool, str):
    """
    Method to check if a flow is valid.

    :param flow:
    :return:
    """
    pattern = re.compile("^[a-zA-Z0-9_.-]{3,128}$")
    count_input = 0
    if_input_defined = False
    if_output_defined = False
    node_service = NodeService()
    operation_manager = FlowOperationManager()
    input_ops = ["sensor_temperature", "sensor_hall", "sensor_button"]
    process_ops = ["log", "cep_intercept"]
    output_ops = ["exit", "actuator_led", "actuator_speaker"]
    op_names = []
    if len(flow.ops) == 0:
        return False, "Got flow without operations!"
    if not re.match(pattern, flow.name):
        return False, "Flow Name should match following regex: ^[a-zA-Z0-9_.-]{3,128}$!"
    if len(flow.ops) <= 1:
        return False, "Got flow with too less operations!"
    for op in flow.ops:
        if op.name:
            op_names.append(op.name)
        if op.input not in input_ops and op.input:
            return False, "Wrong input operation!"
        if op.input in input_ops:
            count_input += 1
            if_input_defined = True
            if count_input > 1:
                return False, "Only one input is allowed in a flow!"
        if op.process not in process_ops and op.process:
            return False, "Wrong input for process!"
        if not re.match(pattern, op.name):
            return False, "Operation Name should match following regex: ^[a-zA-Z0-9_.-]{3,128}$!"
        if op.output in output_ops:
            if_output_defined = True
        if op.output not in output_ops and op.output:
            return False, "Wrong input for output!"
        if len(operation_manager.detect_nodes_of_step(flow, op.name, node_service.get_all_nodes())) == 0:
            return False, "Can not execute node step execution!"
    if not if_output_defined:
        return False, "No output defined!"
    if not if_input_defined:
        return False, "No input defined!"
    op_names_set = set(op_names)
    if len(op_names_set) != len(op_names):
        return False, "Operation names need to be unique per flow!"
    return True,

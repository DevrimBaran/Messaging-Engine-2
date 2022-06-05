import re
from typing import List

from pime2.entity import FlowEntity


def is_flow_valid(flow: FlowEntity) -> (bool, List[str]):
    """
    Method to check if a flow is valid.

    :param flow:
    :return:
    """
    pattern = re.compile("^[a-zA-Z0-9_.-]{3,128}$")
    count_input = 0
    if_input_defined = False
    if_output_defined = False
    if len(flow.ops) == 0:
        return False, ["Got flow without operations!"]
    elif not re.match(pattern, flow.name):
        return False, ["Flow Name should match following regex: ^[a-zA-Z0-9_.-]{3,128}$!"]
    elif len(flow.ops) <= 1:
        return False, ["Got flow with too less operations!"]
    for op in flow.ops:
        if op.input not in ["sensor_temperature", "sensor_hall", "sensor_button"] and op.input:
            return False, ["Wrong input operation!"]
        if op.input in ["sensor_temperature", "sensor_hall", "sensor_button"]:
            count_input += 1
            if_input_defined = True
            if count_input > 1:
                return False, ["Only one input is allowed in a flow!"]
        if op.process not in ["log", "cep_intercept"] and op.process:
            return False, ["Wrong input for process!"]
        if not re.match(pattern, op.name):
            return False, ["Operation Name should match following regex: ^[a-zA-Z0-9_.-]{3,128}$!"]
        if op.output in ["exit", "actuator_led", "actuator_speaker"]:
            if_output_defined = True
        if op.output not in ["exit", "actuator_led", "actuator_speaker"] and op.output:
            return False, ["Wrong input for output!"]
    if not if_output_defined:
        return False, ["No output defined!"]
    if not if_input_defined:
        return False, ["No input defined!"]
    return True, []

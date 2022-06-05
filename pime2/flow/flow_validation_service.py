import re
from typing import List#

from pime2.entity import FlowEntity


class FlowValidationService:
    """
    This class validates flows and returns the result + validation messages.

    """

    def is_flow_valid(self, flow: FlowEntity) -> (bool, List[str]):
        """
        Method to check if a flow is valid.

        :param flow:
        :return:
        """
        pattern = re.compile("^[a-zA-Z0-9_.-]{3,128}$")
        if len(flow.ops) == 0:
            return False, ["Got flow without operations!"]
        elif not re.match(pattern, flow.name):
            return False, ["Flow Name should match following regex: ^[a-zA-Z0-9_.-]{3,128}$!"]
        elif len(flow.ops) <= 1:
            return False, ["Got flow with too less operations!"]
        for op in flow.ops:
            if op.input != "sensor_temperature" or op.input != "sensor_hall" or op.input != "sensor_button" \
                    or not op.input:
                return False, ["Wrong input operation or input operation is not defined!"]
            elif not op.where:
                return False, ["Instance of where is not defined!"]
            elif op.process != "log" or op.process != "cep_intercept" or not op.process:
                return False, ["Wrong process name or process is empty!"]
            elif "output" not in op:
                return False, ["No output defined!"]
            # TODO: Check in database if skill is present on instance (me-61 needs to be merged in)
            elif not re.match(pattern, op.name):
                return False, ["Operation Name should match following regex: ^[a-zA-Z0-9_.-]{3,128}$!"]
            elif op.output != "exit" or op.output != "actuator_led" or op.output != "actuator_speaker" or not op.output:
                return False, ["wrong input for output or output is empty!"]
        return True, []

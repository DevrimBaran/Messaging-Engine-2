from abc import ABC, abstractmethod
from pime2.sensor.sensor import Operator, SinglePinOperatorArguments, DualPinOperatorArguments
from pime2.common.read_output import DualPinCommonResult, SinglePinCommonResult


# TODO: this is not final or perfect
# TODO: add meaningful properties to these objects
# TODO implement type of actuator


class SinglePinActuator(Operator, ABC):
    """
    Abstract class to represent an abstract sensor.
    Each actuator implements this class.

    """

    def __init__(self, input_arguments: SinglePinOperatorArguments):
        self.args = input_arguments

    @abstractmethod
    def handle(self, input_arg: any) -> SinglePinCommonResult:
        """
        Process current gpio state of a (single?) pin and control the actuator operation.

        :param input_arg:
        :return: success state - if any
        """


class DualPinActuator(Operator, ABC):
    """
    Abstract class to represent an abstract sensor.
    Each actuator implements this class.

    """

    def __init__(self, input_arguments: DualPinOperatorArguments):
        self.args = input_arguments

    @abstractmethod
    def handle(self, input_arg_one: any, input_arg_two) -> DualPinCommonResult:
        """
        Process current gpio state of a (single?) pin and control the actuator operation.

        :param input_arg_one:
        :param input_arg_two:
        :return: success state - if any
        """

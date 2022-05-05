from abc import ABC, abstractmethod
from pime2.sensor.sensor import Operator, SinglePinOperatorArguments, DualPinOperatorArguments


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
    def handle(self, trigger_args: any) -> bool:
        """
        Process current gpio state of a (single?) pin and control the actuator operation.
        TODO: input type is tbd

        :param trigger_args:
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
    def handle(self, trigger_args: any) -> bool:
        """
        Process current gpio state of a (single?) pin and control the actuator operation.
        TODO: input type is tbd

        :param trigger_args:
        :return: success state - if any
        """

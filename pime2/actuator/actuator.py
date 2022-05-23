from abc import ABC, abstractmethod
from enum import Enum
from pime2.common.operator import Operator, SinglePinOperatorArguments, DualPinOperatorArguments
from pime2.common.read_output import DualPinCommonResult


class ActuatorType(Enum):
    """
    Enum to declare which actuator types are supported.
    """
    LED = 1
    SPEAKER = 2


class Actuator(Operator, ABC):
    """
    Abstract class to represent an abstract sensor.
    You should never inherit directly from this class, use SinglePinSensor, DualPinSensor...
    """

    def __init__(self, actuator_type: ActuatorType):
        self.actuator_type = actuator_type


class SinglePinActuator(Actuator, ABC):
    """
    Abstract class to represent an abstract sensor.
    Each actuator implements this class.

    """

    def __init__(self, actuator_type: ActuatorType, input_arguments: SinglePinOperatorArguments):
        super().__init__(actuator_type)
        self.args = input_arguments

    @abstractmethod
    def activate(self, input_arg: any):
        """
        Process current gpio state of a (single?) pin and control the actuator operation.

        :param input_arg:
        :return: success state - if any
        """


class DualPinActuator(Actuator, ABC):
    """
    Abstract class to represent an abstract sensor.
    Each actuator implements this class.

    """

    def __init__(self, actuator_type: ActuatorType, input_arguments: DualPinOperatorArguments):
        super().__init__(actuator_type)
        self.args = input_arguments

    @abstractmethod
    def activate(self, input_arg_one: any, input_arg_two: any) -> DualPinCommonResult:
        """
        Process current gpio state of a (single?) pin and control the actuator operation.

        :param input_arg_one:
        :param input_arg_two:
        :return: success state - if any
        """

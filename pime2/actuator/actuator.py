from abc import ABC, abstractmethod
from enum import Enum
from pime2.common.operator import Operator, SingleGpioOperatorArguments, DualGpioOperatorArguments
from pime2.common.read_output import DualGpioCommonResult


class ActuatorType(Enum):
    """
    Enum to declare which actuator types are supported.
    """
    LED = "LED"
    SPEAKER = "SPEAKER"


class Actuator(Operator, ABC):
    """
    Abstract class to represent an abstract sensor.
    You should never inherit directly from this class, use SinglePinSensor, DualPinSensor...
    """

    def __init__(self, actuator_type: ActuatorType, name: str = "unknown"):
        self.actuator_type = actuator_type
        self.name = name


class SingleGpioActuator(Actuator, ABC):
    """
    Abstract class to represent an abstract sensor.
    Each actuator implements this class.

    """

    def __init__(self, name: str, actuator_type: ActuatorType, input_arguments: SingleGpioOperatorArguments):
        super().__init__(actuator_type, name)
        self.args = input_arguments

    @abstractmethod
    def activate(self, input_arg: any):
        """
        Process current gpio state of a (single?) pin and control the actuator operation.

        :param input_arg:
        :return: success state - if any
        """


class DualGpioActuator(Actuator, ABC):
    """
    Abstract class to represent an abstract sensor.
    Each actuator implements this class.

    """

    def __init__(self, name: str, actuator_type: ActuatorType, input_arguments: DualGpioOperatorArguments):
        super().__init__(actuator_type, name)
        self.args = input_arguments

    @abstractmethod
    def activate(self, input_arg_one: any, input_arg_two: any) -> DualGpioCommonResult:
        """
        Process current gpio state of a (single?) pin and control the actuator operation.

        :param input_arg_one:
        :param input_arg_two:
        :return: success state - if any
        """
